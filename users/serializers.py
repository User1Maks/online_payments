from rest_framework.serializers import ModelSerializer

from users.models import User


class UserSerializer(ModelSerializer):
    """Сериализатор для модели пользователей."""

    class Meta:
        model = User
        fields = (
            "email",
            "first_name",
            "last_name",
            "phone",
        )


class UserDetailSerializer(ModelSerializer):
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
