from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from users.apps import UsersConfig
from users.views import (
    UserCreateAPIView,
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
    path(
        "login/",
        TokenObtainPairView.as_view(permissions_class=(AllowAny,)),
        name="token_obtain_pair",
    ),
    path(
        "token/refresh/",
        TokenRefreshView.as_view(permissions_class=(AllowAny,)),
        name="token_refresh",
    ),
]
