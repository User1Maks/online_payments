from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from users.apps import UsersConfig
from users.views import (
    PasswordResetConfirm,
    PasswordResetView,
    UserCreateAPIView,
    UserListAPIView,
    UserRetrieveAPIView,
    UserUpdateAPIView,
)

app_name = UsersConfig.name

urlpatterns = [
    path(
        "register/",
        UserCreateAPIView.as_view(permission_classes=(AllowAny,)),
        name="register",
    ),
    path("profile/", UserRetrieveAPIView.as_view(), name="profile"),
    path("update-profile/", UserUpdateAPIView.as_view(), name="update_profile"),
    path("list/", UserListAPIView.as_view(), name="user_list"),
    path(
        "login/",
        TokenObtainPairView.as_view(permission_classes=(AllowAny,)),
        name="token_obtain_pair",
    ),
    path(
        "token/refresh/",
        TokenRefreshView.as_view(permission_classes=(AllowAny,)),
        name="token_refresh",
    ),
    path("reset-password/",
         PasswordResetView.as_view(), name="reset_password"),
    path("reset-password-confirm/",
         PasswordResetConfirm.as_view(), name="reset_password_confirm"),
]
