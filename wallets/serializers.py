from decimal import Decimal

from rest_framework import serializers

from wallets.models import Wallet


class WalletSerializer(serializers.ModelSerializer):
    """Сериализатор для кошелька."""

    class Meta:
        model = Wallet
        fields = ("owner", "wallet_uuid", "account_number",
                  "balance", "created_at")
        read_only_fields = (
            "owner",
            "wallet_uuid",
            "account_number",
            "balance",
            "created_at",
        )


class OperationSerializer(serializers.Serializer):
    """Сериализатор для операций с кошельком."""

    OPERATION_CHOICES = (("DEPOSIT", "Пополнение"), ("WITHDRAW", "Снятие"))
    operation_type = serializers.ChoiceField(
        choices=OPERATION_CHOICES,
        help_text="Выберите операцию: 'DEPOSIT' (пополнение) или "
                  "'WITHDRAW' (снятие)",
    )
    amount = serializers.DecimalField(
        max_digits=15,
        decimal_places=2,
        min_value=Decimal(1.00),
        help_text="Сумма транзакции минимум 1.00 р",
    )
