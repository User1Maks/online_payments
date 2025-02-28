from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from users.models import User
from users.paginators import UserPaginator
from users.permissions import IsManagerUser, IsOwnerUser
from users.serializers import (
    PasswordResetConfirmSerializer,
    ResetPasswordEmailRequestSerializer,
    UserDetailSerializer,
    UserSerializer,
)
from users.tasks import send_reset_password_email


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


class UserRetrieveAPIView(generics.RetrieveAPIView):
    """Endpoint просмотра профиля пользователя."""

    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    permission_classes = (IsManagerUser, IsOwnerUser)


class UserUpdateAPIView(generics.UpdateAPIView):
    """Endpoint для изменения данных пользователя."""

    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    permission_classes = (IsManagerUser, IsOwnerUser)


class PasswordResetView(generics.GenericAPIView):
    """
    Реализует функционал для сброса пароля на указанный email-адрес.
    Алгоритм работы:
    1. Принимает запрос с email пользователя.
    2. Проверяет, существует ли пользователь с указанным email.
    3. Генерирует uid и token для конкретного пользователя.
    4. Формирует ссылку для сброса пароля, используя uid и token.
    5. Отправляет сформированную ссылку пользователю по указанному email.
    """

    serializer_class = ResetPasswordEmailRequestSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]

        if not User.objects.filter(email=email).exists():
            return Response(
                {"error": "Пользователь с таким email не найден."},
                status=status.HTTP_404_NOT_FOUND)

        user = User.objects.get(email=email)
        uid = urlsafe_base64_encode(str(user.uid).encode())

        token = PasswordResetTokenGenerator().make_token(user)
        host = self.request.get_host()
        reset_link = \
            f"http://{host}/users/reset-password-confirm/{uid}/{token}/"

        send_reset_password_email.delay(email, reset_link)
        print("Функция send_reset_password_email отработала")
        print(f"request.data: {request.data}")

        return Response(
            {
                "message": "Ссылка для сброса пароля отправлена на ваш email."
            },
            status=status.HTTP_200_OK)


class PasswordResetConfirm(generics.GenericAPIView):
    """
    Реализует сброс пароля пользователя после проверки uid и token,
    предоставленных в запросе.
    Алгоритм работы:
    1. Сервер принимает POST-запрос с uid, token, и новым паролем
    (new_password).
    2. Проверяет, существует ли пользователь, соответствующий переданному uid.
    3. Проверяет валидность токена сброса пароля для этого пользователя.
    4. Если проверки успешны:
        - Устанавливает новый пароль для пользователя.
        - Сохраняет изменения в базе данных.
    5. Возвращает ответ о том, что пароль был успешно сброшен.
    """
    serializer_class = PasswordResetConfirmSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        uid = serializer.validated_data["uid"]
        token = serializer.validated_data["token"]
        new_password = serializer.validated_data["new_password"]

        decoded_uid = smart_str(urlsafe_base64_decode(uid))
        user = User.objects.get(uid=decoded_uid)

        if not PasswordResetTokenGenerator().check_token(user, token):
            return Response(
                {"error": "Недействительный или истекший токен."},
                status=status.HTTP_400_BAD_REQUEST
            )

        user.set_password(new_password)
        user.save()

        return Response(
            {"message": "Пароль успешно изменен."},
            status=status.HTTP_200_OK
        )
