from decimal import Decimal

import pytest
from django.urls import reverse
from rest_framework import status

from wallets.tasks import update_wallet_balance


@pytest.mark.django_db
def test_wallet_anonymous_user_permissions(api_client, wallet):
    """Тест на достуа анонимного пользователя к API."""
    create_url = reverse("wallets:wallet_create")
    response_create = api_client.post(create_url, data={})
    assert response_create.status_code == status.HTTP_401_UNAUTHORIZED

    detail_url = reverse("wallets:wallet_detail",
                         args=[wallet.wallet_uuid])
    response_detail = api_client.get(detail_url)
    assert response_detail.status_code == status.HTTP_401_UNAUTHORIZED

    wallet_operation_url = reverse("wallets:wallet_operation",
                                   args=[wallet.wallet_uuid])
    data = {
        "operation_type": "DEPOSIT",
        "amount": 1000.00
    }
    response_wallet_operation = api_client.post(wallet_operation_url, data=data)
    assert response_wallet_operation.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_wallet_create(aut_user, user):
    """Тест на создание кошелька."""
    url = reverse("wallets:wallet_create")
    response = aut_user.post(url, data={})

    assert response.status_code == status.HTTP_201_CREATED

    expected_keys = {"owner", "wallet_uuid", "account_number", "balance",
                     "created_at"}
    response_keys = set(response.data.keys())
    assert response_keys == expected_keys

    assert response.data["owner"] == user.id
    assert isinstance(response.data["wallet_uuid"], str)
    assert isinstance(response.data["account_number"], str)
    assert len(response.data["account_number"]) == 20
    assert response.data["balance"] == "0.00"
    assert isinstance(response.data["created_at"], str)

    response = aut_user.post(url, data={})
    print(response.data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert isinstance(response.data, list)
    assert len(response.data) > 0


@pytest.mark.django_db
def test_wallet_detail(aut_user, wallet, user):
    """Тест на просмотр информации о кошельке."""
    url = reverse("wallets:wallet_detail", args=[wallet.wallet_uuid])
    response = aut_user.get(url)

    assert response.status_code == status.HTTP_200_OK

    data = response.data
    assert data["owner"] == user.id
    assert isinstance(data["wallet_uuid"], str)
    assert isinstance(data["account_number"], str)
    assert len(data["account_number"]) == 20
    assert data["balance"] == "0.00"
    assert isinstance(data["created_at"], str)


@pytest.mark.django_db
def test_operation_wallet_user(aut_user, wallet):
    """Тест на выполнение операции (пополнение или снятие) владельцем."""
    url = reverse("wallets:wallet_operation",
                  args=[wallet.wallet_uuid])
    data_deposit = {
        "operation_type": "DEPOSIT",
        "amount": "1000.00"
    }
    response = aut_user.post(url, data_deposit)

    assert response.status_code == status.HTTP_200_OK
    update_wallet_balance(wallet.wallet_uuid, **data_deposit)

    wallet.refresh_from_db()
    assert wallet.balance == Decimal("1000.00")

    data_withdraw = {
        "operation_type": "WITHDRAW",
        "amount": 100.00
    }

    response = aut_user.post(url, data_withdraw)

    assert response.status_code == status.HTTP_200_OK
    update_wallet_balance(wallet.wallet_uuid, **data_withdraw)
    wallet.refresh_from_db()
    assert wallet.balance == Decimal("900.00")

    data_withdraw = {
        "operation_type": "WITHDRAW",
        "amount": 10000.00
    }

    response = update_wallet_balance(
        wallet.wallet_uuid,
        **data_withdraw)
    assert response in "Недостаточно средств"
