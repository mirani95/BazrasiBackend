from apps.core.exceptions import ConflictException
from rest_framework.exceptions import APIException
from apps.authorization.api.v1.serializers import (
    RoleSerializer,
    PermissionSerializer,
    UserRelationSerializer,
    PageSerializer
)
from rest_framework.decorators import action
from rest_framework.response import Response
from apps.authorization.models import (
    Role,
    Permissions,
    UserRelations,
    Page
)
from rest_framework import viewsets
from django.db import transaction
from rest_framework import filters
from rest_framework import status


class RoleViewSet(viewsets.ModelViewSet):
    """ Crud Operations For User Roles """

    queryset = Role.objects.all()
    serializer_class = RoleSerializer


class PageViewSet(viewsets.ModelViewSet):
    """ add website pages to system to set permission on it """

    queryset = Page.objects.all()
    serializer_class = PageSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'code']

    @action(
        methods=['delete'],
        detail=True,
        url_name='delete',
        url_path='delete',
        name='delete'
    )
    @transaction.atomic
    def delete(self, request, pk=None):
        """ Full delete of page & permissions of page object """
        try:
            page = self.queryset.get(id=pk)
            permissions = Permissions.objects.filter(page=page)
            permissions.delete()
            page.delete()
            return Response(status=status.HTTP_200_OK)
        except APIException as e:
            return Response(e, status=status.HTTP_204_NO_CONTENT)


class PermissionViewSet(viewsets.ModelViewSet):
    """ Crud Operations for Permissions """

    queryset = Permissions.objects.all()
    serializer_class = PermissionSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['page__name', ]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset().order_by('-create_date'))  # noqa

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        if self.queryset.filter(name=request.data['name'], page_id=request.data['page']).exists():
            raise ConflictException('a permission with this page exists.')
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserRelationViewSet(viewsets.ModelViewSet):
    """ Crud Operations for User Relations """

    queryset = UserRelations.objects.all()
    serializer_class = UserRelationSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset().order_by('-create_date'))  # noqa

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
