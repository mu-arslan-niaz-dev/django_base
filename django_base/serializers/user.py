from django.contrib.auth.models import User
from rest_framework import serializers


class UserCreateSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True, min_length=1)
    email = serializers.EmailField(required=False, allow_blank=True)

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("username already exists")
        return value

    def validate_email(self, value):
        if value and User.objects.filter(email=value).exists():
            raise serializers.ValidationError("email already exists")
        return value

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "is_active",
            "is_staff",
            "date_joined",
        )


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ("password",)


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "is_staff",
            "is_active",
            "is_superuser",
            "email",
            "username",
        )
        extra_kwargs = {
            "first_name": {"required": False},
            "last_name": {"required": False},
            "is_staff": {"required": False},
            "is_active": {"required": False},
            "is_superuser": {"required": False},
            "email": {"required": False},
            "username": {"required": False},
        }

    def validate_username(self, value):
        qs = User.objects.filter(username=value)
        if self.instance is not None:
            qs = qs.exclude(id=self.instance.id)
        if qs.exists():
            raise serializers.ValidationError("username already exists")
        return value

    def validate_email(self, value):
        if not value:
            return value
        qs = User.objects.filter(email=value)
        if self.instance is not None:
            qs = qs.exclude(id=self.instance.id)
        if qs.exists():
            raise serializers.ValidationError("email already exists")
        return value
