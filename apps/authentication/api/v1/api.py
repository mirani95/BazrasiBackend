import random
import typing

from django.core.cache import cache
from django.db import transaction
from rest_framework import filters
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.authentication.api.v1.serializers.jwt import CustomizedTokenObtainPairSerializer
from apps.authentication.api.v1.serializers.serializer import (
    CitySerializer,
    ProvinceSerializer,
    OrganizationTypeSerializer,
    OrganizationSerializer,
    UserSerializer,
    BankAccountSerializer,
)
from apps.authentication.models import (
    User,
    City,
    Province,
    Organization,
    OrganizationType,
    BankAccountInformation,
    BlacklistedAccessToken
)
from apps.authentication.tools import get_token_jti
from apps.authorization.api.v1 import api as authorize_view
from common.helpers import get_organization_by_user
from common.sms import send_sms
from common.tools import CustomOperations


class CustomizedTokenObtainPairView(TokenObtainPairView):
    """ Generate Customize token """
    serializer_class = CustomizedTokenObtainPairSerializer


class UserViewSet(ModelViewSet):
    """ Crud operations for user model """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'mobile', 'national_code']
    permission_classes = [AllowAny]

    @transaction.atomic
    def create(self, request, *args, **kwargs):

        """
        Customizing create user & bank account information with
        permission levels
        """

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if 'user_relations' in request.data.keys():
                user_relations = CustomOperations().custom_create(  # create user relations
                    user=user,
                    request=request,
                    view=authorize_view.UserRelationViewSet(),
                    data_key='user_relations',
                )
            else:
                user_relations = {}
            if 'bank_account' in request.data.keys():
                bank_account = CustomOperations().custom_create(  # create user bank account info
                    user=user,
                    request=request,
                    view=BankAccountViewSet(),
                    data_key='bank_account'
                )
            else:
                bank_account = {}
            serializer_data = serializer.data
            serializer_data.update({
                'user_relations': user_relations,  # noqa
                'bank_account': bank_account  # noqa
            })
            return Response(serializer_data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_403_FORBIDDEN)

    @transaction.atomic
    def update(self, request, pk=None, *args, **kwargs):
        """
        Customizing update user & bank account info with
        permission levels
        """
        serializer = self.serializer_class(data=request.data, instance=self.get_object(), partial=True)
        if serializer.is_valid():
            user = serializer.save()

            if 'organization' in request.data.keys():  # noqa
                organization = CustomOperations().custom_update(  # update organization for user
                    request=request,
                    view=OrganizationViewSet(),
                    data_key='organization',
                    obj_id=request.data['organization']['id']
                )
            else:
                organization = {}
            if 'user_relations' in request.data.keys():
                user_relations = CustomOperations().custom_update(  # update user relations
                    user=user,
                    request=request,
                    view=authorize_view.UserRelationViewSet(),
                    data_key='user_relations',
                    obj_id=request.data['user_relations']['id']
                )
            else:
                user_relations = {}
            if 'bank_account' in request.data.keys():
                bank_account = CustomOperations().custom_update(  # update user bank account info
                    user=user,
                    request=request,
                    view=BankAccountViewSet(),
                    data_key='bank_account',
                    obj_id=request.data['bank_account']['id']
                )
            else:
                bank_account = {}
            serializer_data = serializer.data
            serializer_data.update({
                'organization': organization,
                'user_relations': user_relations,  # noqa
                'bank_account': bank_account  # noqa
            })
            return Response(serializer_data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        methods=['get'],
        detail=False,
        url_name='profile',
        url_path='profile',
        name='profile',
        # permission_classes=[AllowAny]
    )
    def profile(self, request):
        serializer = authorize_view.UserRelationSerializer(
            authorize_view.UserRelations.objects.get(user=request.user,trash=False)
        )
        return Response(serializer.data, status.HTTP_200_OK)


class CityViewSet(ModelViewSet):
    """ Crud operations for city model """  #
    queryset = City.objects.all()
    serializer_class = CitySerializer

    @action(
        methods=['get'],
        detail=False,
        url_name='get_city',
        url_path='get_city',
        name='get_city',
        # permission_classes=[AllowAny]
    )
    def get_city(self, request, *args, **kwargs):
        """ return list of cities by province """

        serializer = self.serializer_class(
            self.queryset.filter(
                province_id=int(request.GET['province'])
            ), many=True
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProvinceViewSet(ModelViewSet):
    """ Crud operations for province model """  #
    queryset = Province.objects.all()
    serializer_class = ProvinceSerializer

    @action(
        methods=['get'],
        detail=False,
        url_name='get_province',
        url_path='get_province',
        name='get_province',
        # permission_classes=[AllowAny]
    )
    def get_province(self, request):
        query = self.queryset
        ser_data = self.serializer_class(query, many=True).data
        return Response(ser_data, status=status.HTTP_200_OK)


class OrganizationTypeViewSet(ModelViewSet):
    """ Crud operations for Organization Type model """  #
    queryset = OrganizationType.objects.all()
    serializer_class = OrganizationTypeSerializer


class OrganizationViewSet(ModelViewSet):
    """ Crud operations for organization model """  #
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer

    def get_all_org_child(self, org):
        descendants = []
        children = org.parents.all()
        for child in children:
            descendants.append(child)
            descendants.extend(self.get_all_org_child(child))
        return descendants

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        """
        @create Organization by user
        """
        serializer = self.serializer_class(data=request.data['organization'])

        if serializer.is_valid():
            organization = serializer.save()

            if 'user_relations' in request.data.keys():
                user_relations = CustomOperations().custom_create(  # create user relations
                    request=request,
                    view=authorize_view.UserRelationViewSet(),
                    data_key='user_relations',
                    additional_data={'organization': organization.id}  # noqa
                )
                serializer_data = serializer.data
                serializer_data.update(
                    {'user_relations': user_relations}
                )
                return Response(serializer_data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        """ update organization data """

        partial = kwargs.pop('partial', False)
        instance = self.get_object()  # get organization instance
        serializer = self.get_serializer(
            instance,
            data=request.data['organization'],
            partial=partial
        )
        serializer.is_valid(raise_exception=True)
        organization = serializer.save()

        if 'user_relations' in request.data.keys():
            user_relations = CustomOperations().custom_update(  # update user relations
                request=request,
                view=authorize_view.UserRelationViewSet(),
                data_key='user_relations',
                additional_data={'organization': organization.id}  # noqa
            )
            serializer_data = serializer.data
            serializer_data.update(
                {'user_relations': user_relations}
            )
            return Response(serializer_data, status=status.HTTP_200_OK)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        methods=['get'],
        detail=False,
        url_path='organizations_by_province',
        url_name='organizations_by_province',
        name='organizations_by_province',
    )
    @transaction.atomic
    def get_organizations_by_province(self, request):
        """ list of organizations by province """

        queryset = self.queryset.filter(province=int(request.GET['province']))

        page = self.paginate_queryset(queryset)  # paginate queryset

        if page is not None:
            serializer = self.serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        methods=['get'],
        detail=False,
        url_path='child_organizations',
        url_name='child_organizations',
        name='child_organizations'
    )
    @transaction.atomic
    def get_child_organizations(self, request):
        organization = get_organization_by_user(request.user)
        child_organizations = self.get_all_org_child(organization)

        page = self.paginate_queryset(child_organizations)  # paginate queryset

        if page is not None:
            serializer = self.serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)


class BankAccountViewSet(ModelViewSet):
    """ Crud operations for bank account model """  #
    queryset = BankAccountInformation.objects.all()
    serializer_class = BankAccountSerializer


class GeneralOTPViewSet(ModelViewSet):
    """ general OTP user authorization """

    user_relations_queryset = authorize_view.UserRelations.objects.all()
    organization_queryset = Organization.objects.all()
    user_queryset = User.objects.all()
    user_serializer = UserSerializer
    organization_serializer = OrganizationSerializer
    user_relations_serializer = authorize_view.UserRelationSerializer

    @classmethod
    def get_user_mobile(cls, data: dict) -> typing.Any:
        """ find user mobile in multiple modes like from organization """

        if data['get_mobile_type'] == 'organization':
            # get user mobile by his/her organization
            user_mobile = cls.user_relations_queryset.filter(
                organization_id=int(data['object_id']),
                role__role_name='Management').first().user.mobile
            return user_mobile

        if data['get_mobile_type'] == 'general':
            return data['mobile']

    @action(
        methods=['post'],
        detail=False,
        url_path='send_otp',
        url_name='send_otp',
        name='send_otp'
    )
    @transaction.atomic
    def send_otp(self, request):
        """
        This module is for sending otp in whole project and different parts
        like send otp code to user by organization or by general user mobile
        """

        mobile = self.get_user_mobile(
            data=request.data
        )

        # generate random integer and message for otp code
        random_number = random.randint(10000, 99999)
        message = f'کد احراز شما : {random_number}'  # noqa

        # caching code
        if 'timeout' in request.data.keys():
            cache.set(f"{random_number}", str(random_number), timeout=60 * int(request.data['timeout']))
        else:
            cache.set(f"{random_number}", str(random_number), timeout=60 * 3)

        sms_response = send_sms(mobile=mobile, message=message)
        return Response(status=status.HTTP_200_OK)

    @action(
        methods=['post'],
        detail=False,
        url_name='check_otp',
        url_path='check_otp',
        name='check_otp'
    )
    def check_otp(self, request):
        """ Check sent otp code to user """

        entered_code = request.data['code']
        cached_code = cache.get(entered_code)

        if entered_code == cached_code:
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_403_FORBIDDEN)


class LogoutView(APIView):
    """ logout user """

    permission_classes = [IsAuthenticated]

    def post(self, request):  # noqa
        token_str = request.auth  # access token from header
        jti, user_id = get_token_jti(str(token_str))

        if not jti:
            return Response({'detail': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

        BlacklistedAccessToken.objects.get_or_create(jti=jti, defaults={
            'token': token_str,
            'user_id': user_id,
        })

        return Response({'detail': 'Access token blacklisted.'}, status=status.HTTP_200_OK)
