from rest_framework import serializers

from wallets.models import Wallet


class WalletSerializer(serializers.ModelSerializer):
    """Сериализатор для кошелька."""

    class Meta:
        model = Wallet
        fields = ("owner", "wallet_uuid", "account_number",
                  "balance", "created_at")
        read_only_fields = (
            "wallet_uuid",
            "account_number",
            "balance",
            "created_at",
        )


class WalletCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания кошелька."""

    class Meta:
        model = Wallet
        fields = ("wallet_uuid", "balance")
        read_only_fields = ("wallet_uuid", "account_number", "balance",
                            "created_at")


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
        min_value=1.00,
        help_text="Сумма транзакции минимум 1.00 р",
    )
