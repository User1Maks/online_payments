from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """Права доступа владельца кошелька."""

    def has_permission(self, request, view):
        """Проверка авторизован ли пользователь."""
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """Проверяет принадлежит ли кошелек пользователю."""
        return request.user == obj.owner
