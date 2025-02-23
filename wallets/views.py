from rest_framework import generics

from wallets.models import Wallet
from wallets.serializers import WalletSerializer


class WalletCreateAPIView(generics.CreateAPIView):
    """Endpoint добавления кошелька."""

    serializer_class = WalletSerializer


class WalletRetrieveAPIView(generics.RetrieveAPIView):
    """Endpoint для просмотра кошелька."""

    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
