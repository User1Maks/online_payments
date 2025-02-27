import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

NULLABLE = {"blank": True, "null": True}


class User(AbstractUser):
    """Модель пользователя."""

    username = None
    email = models.EmailField(
        unique=True, verbose_name="Email", help_text="Укажите ваш email"
    )
    first_name = models.CharField(max_length=50, verbose_name="Имя")
    last_name = models.CharField(
        max_length=50, verbose_name="Фамилия", help_text="Введите фамилию"
    )
    surname = models.CharField(
        max_length=50, **NULLABLE, verbose_name="Отчество",
        help_text="Введите отчество"
    )
    phone = PhoneNumberField(
        unique=True, verbose_name="Номер телефона",
        help_text="Введите номер телефона"
    )
    date_of_birth = models.DateField(
        **NULLABLE, verbose_name="Дата рождения",
        help_text="Введите дату рождения"
    )
    uid = models.UUIDField(
        verbose_name="UID пользователя",
        default=uuid.uuid4,
        editable=False,
        unique=True

    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.first_name} {self.first_name[:1]}. - {self.email}"

    def save(self, *args, **kwargs):
        if not self.uid:
            self.uid = uuid.uuid4()

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
