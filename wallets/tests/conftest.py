import pytest
from rest_framework.test import APIClient

from users.models import User
from wallets.models import Wallet


@pytest.fixture
def api_client():
    """Фикстура клиента."""
    return APIClient()


@pytest.fixture
def user():
    """Фикстура пользователя."""
    user = User.objects.create(
        email="testsuser@example.com",
        password="test-pass",
        first_name="Test",
        last_name="Testov",
        surname="Testovich",
        phone="+7-800-555-35-35",
        date_of_birth="1997-03-15"
    )
    return user


@pytest.fixture
def manager():
    """Фикстура менеджера."""
    manager = User.objects.create(
        email="testsmanager@example.com",
        password="test-password",
        first_name="Manager",
        last_name="Test",
        surname="Managerovich",
        phone="+7-800-333-35-35",
        date_of_birth="1995-02-10"
    )
    manager.is_staff = True
    return manager


@pytest.fixture
def aut_user(api_client, user):
    """Фикстура авторизованного пользователя."""
    api_client.force_authenticate(user=user)
    return api_client


@pytest.fixture
def aut_manager(api_client, manager):
    """Фикстура авторизованного менеджера."""
    api_client.force_authenticate(user=manager)
    return api_client


@pytest.fixture
def wallet(user):
    """Фикстура кошелька."""
    wallets = Wallet.objects.create(
        owner=user,
        account_number="01234567890123456789",
        balance=0.00,
        created_at=(2025, 2, 25)
    )
    return wallets


@pytest.fixture(autouse=True)
def disable_celery_tasks(monkeypatch):
    """Отключает celery для тестов."""
    monkeypatch.setattr("celery.app.task.Task.apply_async",
                        lambda *args, **kwargs: None)
