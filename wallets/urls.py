from django.urls import path

from wallets.apps import WalletsConfig
from wallets.views import WalletCreateAPIView, WalletRetrieveAPIView

app_name = WalletsConfig.name

urlpatterns = [
    path("create/", WalletCreateAPIView.as_view(), name="wallet_create"),
    path("detail/<int:pk>/", WalletRetrieveAPIView.as_view(), name="wallet_detail"),
]
