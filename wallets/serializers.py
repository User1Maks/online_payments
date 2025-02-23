from rest_framework import serializers

from wallets.models import Wallet


class WalletSerializer(serializers.ModelSerializer):
    """Сериализатор для кошелька."""

    class Meta:
        model = Wallet
        fields = ("owner",)
        read_only_fields = (
            "account_number",
            "balance",
            "created_at",
        )
