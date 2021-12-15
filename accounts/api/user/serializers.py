from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.reverse import reverse as api_reverse

from accounts.models import Profile

User = get_user_model()


class UserDetailSerializer(serializers.ModelSerializer):
    uri = serializers.SerializerMethodField(read_only=True)
    image_uri = serializers.SerializerMethodField(read_only=True)
    uuid = serializers.SerializerMethodField()
    account_type = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'uuid',
            'email',
            'image_uri',
            'account_type',
            'uri',
        ]

    def get_uri(self, obj):
        request = self.context.get('request')
        return api_reverse("api-user:detail", kwargs={"username": obj.username}, request=request)

    def get_image_uri(self, obj: User):
        instance = Profile.objects.get(user=obj)
        return instance.image.url

    def get_uuid(self, obj: User):
        instance = Profile.objects.get(user=obj)
        return instance.uuid

    def get_account_type(self, obj: User):
        instance = Profile.objects.get(user=obj)
        return instance.account_type