import datetime
from abc import ABC

import phonenumbers
from django.contrib.auth import get_user_model
from django.contrib.auth.models import update_last_login
from django.utils import timezone
from django_countries.fields import Country
from phonenumber_field.serializerfields import PhoneNumberField
from phonenumbers.phonenumberutil import region_code_for_country_code

from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
from rest_framework.reverse import reverse as api_reverse

from accounts.backend import EmailBackend
from accounts.models import Profile

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_response_payload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER
expire_delta = api_settings.JWT_REFRESH_EXPIRATION_DELTA

User = get_user_model()


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        username = data.get("username", )
        password = data.get("password", )
        user = EmailBackend.authenticate(username=username, password=password)
        if user is None:
            raise serializers.ValidationError('User with username and password does not exists.')
        try:
            payload = jwt_payload_handler(user)
            jwt_token = jwt_encode_handler(payload)
            update_last_login(None, user)
        except User.DoesNotExist:
            raise serializers.ValidationError('User with given email and password does not exists')
        return {
            'user': user,
            'token': jwt_token
        }


class UserRegisterSerializer(serializers.ModelSerializer):
    phone = PhoneNumberField(write_only=True)
    firstName = serializers.CharField(write_only=True)
    lastName = serializers.CharField(write_only=True)
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    token = serializers.SerializerMethodField(read_only=True)
    expires = serializers.SerializerMethodField(read_only=True)
    message = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        error_message = ''
        fields = [
            'username',
            'firstName',
            'lastName',
            'email',
            'phone',
            'password',
            'password2',
            'token',
            'expires',
            'message',
        ]
        extra_kwargs = {'password': {'write_only': True}}

    def get_message(self, obj):
        return "Thank you for registering"

    def get_expires(self, obj):
        return timezone.now() + expire_delta - datetime.timedelta(seconds=200)

    def validate_email(self, value):
        qs = User.objects.filter(email__iexact=value)
        if qs.exists():
            raise serializers.ValidationError("User with this email already exists")
        return value

    def get_token(self, obj):  # instance of the model
        user = obj
        payload = jwt_payload_handler(user)
        return jwt_encode_handler(payload)

    def validate(self, data):
        pw = data.get('password', )
        pw2 = data.pop('password2')
        if pw != pw2:
            raise serializers.ValidationError("Passwords must match")
        return data

    def create(self, validated_data):
        user_obj = User(
            email=validated_data.get('email', ),
            username=validated_data.get('username', ),
            first_name=validated_data.get('firstName', ),
            last_name=validated_data.get('lastName', ),
            # first_name=str(validated_data.get('fullName')).split()[0],
            # last_name=str(validated_data.get('fullName')).split()[1],
        )
        user_obj.set_password(validated_data.get('password', ))
        user_obj.is_active = True
        user_obj.save()

        pn = phonenumbers.parse(str(validated_data.get('phone', )))
        country_affix = region_code_for_country_code(pn.country_code)
        country_inst = Country(code=country_affix)

        profile = Profile.objects.get(user=user_obj)
        profile.phone = validated_data.get('phone', )
        profile.country = country_inst
        profile.country_flag = country_inst.flag
        profile.save()

        return user_obj


class UserPublicSerializer(serializers.ModelSerializer):
    uri = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'uri'
        ]

    def get_uri(self, obj):
        request = self.context.get('request')
        return api_reverse("api-user:detail", kwargs={"username": obj.username}, request=request)

"""
>>> person = Person(name='Chris', country='NZ')
>>> person.country
Country(code='NZ')
>>> person.country.name
'New Zealand'
>>> person.country.flag
'/static/flags/nz.gif'
{
    "username": "akapa",
    "email": "akapatemisan50@gmail.com",
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxNCwidXNlcm5hbWUiOiJha2FwYSIsImV4cCI6MTYxODQxOTMyMiwiZW1haWwiOiJha2FwYXRlbWlzYW41MEBnbWFpbC5jb20ifQ.phdZ3rnkBtUT-P3pFIuDRRNGudp5dVAEsd4HSgiPecE",
    "expires": "2021-04-14T16:52:02.925626Z",
    "message": "Thank you for registering. Please verify your email before continuing."
}
{
'username': 'akapa', 
'email': 'akapatemisan50@gmail.com', 
'phone': PhoneNumber(
    country_code=234, 
    national_number=9013128381, 
    extension=None, 
    italian_leading_zero=None, 
    number_of_leading_zeros=None, 
    country_code_source=1, 
    preferred_domestic_carrier_code=None
    ), 
 'password': 'pass=123'
 }
{'username': 'akapa', 'full_name': 'Akapa Temisan', 'email': 'akapatemisan50@gmail.com', 'phone': PhoneNumber(country_code=234, national_number=7010550325, extension=None, italian_leading_zero=None, number_of_leading_zeros=None, country_code_source=1, preferred_domestic_carrier_code=None), 'password': 'pass=123'}
"""

# ModelClass.objects.create(**validated_data)
# User.objects.create(username=username, password=password, password2=password2)
