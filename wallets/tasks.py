from decimal import Decimal

from celery import shared_task
from django.db import transaction

from .models import Wallet


@shared_task
def update_wallet_balance(wallet_uuid, operation_type, amount):
    """Фоновая задача для обновления баланса кошелька."""
    try:
        amount = Decimal(amount)

        with transaction.atomic():
            wallet = Wallet.objects.select_for_update().get(
                wallet_uuid=wallet_uuid)

            if operation_type == "DEPOSIT":
                wallet.balance += amount
            elif operation_type == "WITHDRAW":
                if wallet.balance < amount:
                    return "Недостаточно средств"
                wallet.balance -= amount

            wallet.save()
        return (f"Операция выполнена успешно."
                f" Текущий баланс {wallet.balance} руб")
    except Wallet.DoesNotExist:
        return "Кошелек не найден."
