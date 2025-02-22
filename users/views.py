from rest_framework import generics
from rest_framework.permissions import AllowAny

from users.models import User
from users.serializers import UserDetailSerializer, UserSerializer


class UserCreateAPIView(generics.CreateAPIView):
    """Endpoint создания пользователя."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        """Зашифровывает пароли в базе данных и делает пользователя активным."""
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserRetrieveAPIView(generics.RetrieveAPIView):
    """Endpoint просмотра профиля пользователя."""

    queryset = User.objects.all()
    serializer_class = UserDetailSerializer

    def get_object(self):
        return self.request.user


class UserUpdateAPIView(generics.UpdateAPIView):
    """Endpoint для изменения данных пользователя."""

    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
