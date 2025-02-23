from django.db import models

from users.models import User
from wallets.services import generate_unique_account_number


class Wallet(models.Model):
    """Модель кошелька пользователя."""

    owner = models.OneToOneField(
        User,
        verbose_name="Владелец",
        related_name="wallet",
        on_delete=models.PROTECT,
        help_text="Владелец кошелька",
    )
    account_number = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="Номер счета",
        editable=False,
        default=generate_unique_account_number,
    )
    balance = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0.00,
        verbose_name="Баланс",
        editable=False,
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата и время создания", editable=False
    )

    def __str__(self):
        return f"{self.owner} - {self.balance} руб"

    class Meta:
        verbose_name = "Кошелек"
        verbose_name_plural = "Кошельки"
