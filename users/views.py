from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import AllowAny

from users.models import User
from users.paginators import UserPaginator
from users.permissions import IsManagerUser, IsOwnerUser
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


class UserListAPIView(generics.ListAPIView):
    """Endpoint просмотра списка пользователей."""

    queryset = User.objects.all().order_by("first_name", "last_name")
    serializer_class = UserSerializer
    permission_classes = (IsManagerUser,)
    pagination_class = UserPaginator


class UserRetrieveAPIView(generics.RetrieveAPIView):
    """Endpoint просмотра профиля пользователя."""

    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    permission_classes = (IsManagerUser, IsOwnerUser)
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    filterset_fields = ("first_name", "last_name")
    ordering_fields = (
        "first_name",
        "last_name",
        "ordering_fields",
    )
    search_fields = (
        "first_name",
        "last_name",
    )


class UserUpdateAPIView(generics.UpdateAPIView):
    """Endpoint для изменения данных пользователя."""

    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    permission_classes = (IsManagerUser, IsOwnerUser)
