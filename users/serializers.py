from rest_framework import serializers
from users.models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "phone",
            "image",
            "notification_token",
        ]
        extra_kwargs = {"password": {"write_only": True}, "email": {"required": True}}
