import random
import string


def generate_unique_account_number():
    """Генерирует уникальный 20-значный расчетный номер счета."""
    from .models import Wallet

    while True:
        account_number = "".join(random.choices(string.digits, k=20))
        if not Wallet.objects.filter(account_number=account_number).exists():
            return account_number
