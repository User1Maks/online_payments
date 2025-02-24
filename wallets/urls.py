from django.urls import path

from wallets.apps import WalletsConfig
from wallets.views import (
    WalletCreateAPIView,
    WalletOperationAPIView,
    WalletRetrieveAPIView,
)

app_name = WalletsConfig.name

urlpatterns = [
    path("wallet-create/", WalletCreateAPIView.as_view(), name="wallet_create"),
    path(
        "wallets/<uuid:wallet_uuid>",
        WalletRetrieveAPIView.as_view(),
        name="wallet_detail",
    ),
    path(
        "wallets/<uuid:wallet_uuid>/operation",
        WalletOperationAPIView.as_view(),
        name="wallet_operation",
    ),
]
