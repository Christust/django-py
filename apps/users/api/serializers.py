from rest_framework import serializers
from apps.users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

    def validate_email(self, value):
        if "dev" in value:
            raise serializers.ValidationError("El email no puede contener dev")
        return value

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        update_user = super().update(instance, validated_data)
        update_user.set_password(validated_data["password"])
        update_user.save()
        return update_user


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "name", "last_name"]

    def to_representation(self, instance):
        return {
            "id": instance.id,
            "user": instance.username,
            "name": instance.name,
            "last_name": instance.last_name,
        }

class UserTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email", "last_name", "name"]