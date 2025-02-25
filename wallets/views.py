from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from .models import Wallet
from .permissions import IsOwner
from .serializers import (
    OperationSerializer,
    WalletSerializer,
)
from .tasks import update_wallet_balance


class WalletCreateAPIView(generics.CreateAPIView):
    """Endpoint добавления кошелька."""

    serializer_class = WalletSerializer

    def perform_create(self, serializer):
        """Автоматически добавляет владельца кошелька."""
        user = self.request.user

        if hasattr(user, "wallet"):
            raise ValidationError(
                f"У Вас уже есть кошелек"
                f" номер счета: {user.wallet.account_number}"
            )

        serializer.save(owner=self.request.user)

    def post(self, request, *args, **kwargs):
        """Обрабатываем POST-запрос на создание кошелька."""
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WalletRetrieveAPIView(generics.RetrieveAPIView):
    """Endpoint для просмотра кошелька."""

    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    lookup_field = "wallet_uuid"


class WalletOperationAPIView(generics.GenericAPIView):
    """Endpoint для выполнения операции с кошельком (пополнение или снятие)."""

    serializer_class = OperationSerializer
    permission_classes = (IsOwner,)

    def post(self, request, wallet_uuid):
        """Выполняет операцию (пополнение или снятия) средств."""
        try:
            wallet = Wallet.objects.get(wallet_uuid=wallet_uuid)
        except Wallet.DoesNotExist:
            return Response(
                {"detail": "Кошелек не найден."},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"detail": "Неверный формат данных"},
                status=status.HTTP_400_BAD_REQUEST
            )

        operation_type = serializer.validated_data["operation_type"]
        amount = serializer.validated_data["amount"]

        if operation_type == "WITHDRAW" and wallet.balance < amount:
            return Response(
                {"detail": "Недостаточно средств"},
                status=status.HTTP_400_BAD_REQUEST
            )
        print("REQUEST DATA:", request.data)

        update_wallet_balance.delay(wallet.wallet_uuid, operation_type, amount)

        return Response(
            {"message": "Операция выполнена успешно!"},
            status=status.HTTP_200_OK
        )
