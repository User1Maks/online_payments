from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для модели пользователей."""

    class Meta:
        model = User
        fields = (
            "email",
            "first_name",
            "last_name",
            "surname",
            "phone",
            "date_of_birth",
        )


class UserDetailSerializer(serializers.ModelSerializer):
    """Сериализатор для просмотра профиля пользователя."""

    class Meta:
        model = User
        fields = (
            "email",
            "first_name",
            "last_name",
            "surname",
            "phone",
            "date_of_birth",
        )


class ResetPasswordEmailRequestSerializer(serializers.Serializer):
    """Serializers для получения email от клиента для сброса пароля."""
    email = serializers.EmailField(min_length=2)

    class Meta:
        fields = ("email",)


class PasswordResetConfirmSerializer(serializers.Serializer):
    """
    Serializers для обработки запроса на установку нового пароля с
    использованием UID и токена.
    """
    uid = serializers.CharField(min_length=1, write_only=True)
    token = serializers.CharField(min_length=1, write_only=True)
    new_password = serializers.CharField(min_length=6, max_length=68,
                                         write_only=True)

    class Meta:
        fields = ("uid", "token", "password",)
