from django.contrib.auth.hashers import make_password
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
            "password",
        ]
        extra_kwargs = {
            "password": {"write_only": True, "required": False},
            "email": {"required": True},
        }

    def validate_password(self, value):
        # Si es create es obligatorio mandar pass
        if self.instance is None and not value:
            raise serializers.ValidationError(
                "El password es obligatorio al crear un usuario."
            )
        # Si es update no se obliga
        if self.instance and not value:
            return None
        return value

    def create(self, validated_data):
        raw_password = validated_data.pop("password")
        # encriptamos la pass
        validated_data["password"] = make_password(raw_password)
        user = CustomUser.objects.create(**validated_data)
        return user

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
