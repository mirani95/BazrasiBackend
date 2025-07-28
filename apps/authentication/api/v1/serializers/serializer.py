from apps.authorization.api.v1.serializers import (
    UserRelationSerializer,
    PermissionSerializer,
    RoleSerializer
)
from rest_framework import serializers
from apps.authentication.models import (
    User,
    City,
    Province,
    Organization,
    OrganizationType,
    OrganizationStats,
    BankAccountInformation
)
from apps.authorization import models as authorize_models
import typing


class CitySerializer(serializers.ModelSerializer):
    """ Serialize city data """

    class Meta:
        model = City
        fields = [
            'id',
            'name',
        ]


class ProvinceSerializer(serializers.ModelSerializer):
    """ Serialize province data """

    class Meta:
        model = Province
        fields = [
            'id',
            'name',
        ]


class BankAccountSerializer(serializers.ModelSerializer):
    """ Serialize bank account data """

    class Meta:
        model = BankAccountInformation
        fields = [
            'id',
            'user',
            'account',
            'name',
            'card',
            'sheba'
        ]
        extra_kwargs = {
            'user': {'required': False},
            'account': {'required': False},
            'card': {'required': False},
            'sheba': {'required': False}
        }

    def update(self, instance, validated_data):
        """ update user bank account information """
        instance.name = validated_data.get('name', instance.name)
        instance.account = validated_data.get('account', instance.account)
        instance.card = validated_data.get('card', instance.card)
        instance.sheba = validated_data.get('sheba', instance.sheba)
        instance.save()
        return instance


class UserSerializer(serializers.ModelSerializer):
    """ Serialize user data """

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'password',
            'first_name',
            'last_name',
            'is_active',
            'mobile',
            'phone',
            'national_code',
            'birthdate',
            'nationality',
            'ownership',
            'address',
            'photo',
            'province',
            'city',
            'otp_status',
            'visible_password',
        ]
        extra_kwargs = {
            'password': {
                'required': False
            },
            'username': {
                'required': False
            },
            "national_code": {
                'required': False
            },
            "visible_password" : {
                'write_only': True
            }
        }

    def to_representation(self, instance):
        """ Custom output """

        representation = super().to_representation(instance)
        if isinstance(instance, User):
            if instance.bank_information.filter().exists():
                representation['bank_account'] = BankAccountSerializer(
                    instance.bank_information.all(), many=True
                ).data

            if instance.city:
                representation['city_name'] = instance.city.name
            if instance.province:
                representation['province_name'] = instance.province.name


        return representation

    def update(self, instance, validated_data):
        """ update user instance """
        instance.username = validated_data.get('username', instance.username)
        instance.password = validated_data.get('password', instance.password)
        instance.first_name = validated_data.get('first_name')
        instance.last_name = validated_data.get('last_name')
        instance.is_active = validated_data.get('is_active')
        instance.mobile = validated_data.get('mobile')
        instance.phone = validated_data.get('phone')
        instance.national_code = validated_data.get('national_code')
        instance.birthdate = validated_data.get('birthdate')
        instance.nationality = validated_data.get('nationality')
        instance.ownership = validated_data.get('ownership')
        instance.address = validated_data.get('address')
        instance.photo = validated_data.get('photo')
        instance.province = validated_data.get('province', instance.province)
        instance.city = validated_data.get('province', instance.province)
        instance.otp_status = validated_data.get('otp_status')
        instance.visible_password = validated_data.get('visible_password',instance.password)
        instance.save()

        return instance

    @staticmethod
    def update_relations(user: object, relation_data: dict, bank_data: dict) -> typing.Any:
        """
            update user relations & bank account for user
        """
        user_relation = UserRelationSerializer(data=relation_data)  # Create user relation
        if user_relation.is_valid(raise_exception=True):
            user_relation_obj = user_relation.update(
                authorize_models.UserRelations.objects.get(user=user),
                validated_data=relation_data
            )

        bank_info = BankAccountSerializer(data=bank_data)  # Create user bank information
        if bank_info.is_valid(raise_exception=True):
            bank_obj = bank_info.update(
                BankAccountInformation.objects.get(id=bank_data['id']),
                validated_data=bank_data
            )

        return user_relation_obj, bank_obj  # noqa


class OrganizationTypeSerializer(serializers.ModelSerializer):
    """ Serialize organization type data """

    class Meta:
        model = OrganizationType
        fields = [
            'id',
            'key',
            'name',
        ]


class OrganizationSerializer(serializers.ModelSerializer):
    """ Serialize organization data """

    class Meta:
        model = Organization
        fields = [
            'id',
            'name',
            'type',
            'province',
            'city',
            'parent_organization',
            'national_unique_id',
            'company_code',
            'field_of_activity'
        ]
        extra_kwargs = {}

    def to_representation(self, instance):
        """ Custom output """
        representation = super().to_representation(instance)
        if isinstance(instance, Organization):
            representation['province'] = ProvinceSerializer(instance.province).data
            representation['city'] = CitySerializer(instance.city).data
            representation['type'] = OrganizationTypeSerializer(instance.type).data
            if instance.parent_organization:
                representation['parent_organization'] = OrganizationSerializer(
                    instance.parent_organization
                ).data
        return representation

    def update(self, instance, validated_data):
        """ update user organization information """  # noqa
        instance.name = validated_data.get('name', instance.name)
        instance.type = validated_data.get('type', instance.type)
        instance.province = validated_data.get('province', instance.province)
        instance.city = validated_data.get('city', instance.city)
        instance.parent_organization = validated_data.get('parent_organization', instance.parent_organization)
        instance.national_unique_id = validated_data.get('national_unique_id', instance.national_unique_id)
        instance.save()
        return instance


class OrganizationStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganizationStats
        fields = '__all__'
