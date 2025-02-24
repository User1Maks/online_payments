from rest_framework.permissions import BasePermission


class IsOwnerUser(BasePermission):
    """Права доступа владельца кошелька."""

    edit_methods = ("DELETE",)

    def has_object_permission(self, request, view, obj):
        if request.method not in self.edit_methods:
            return request.user == obj


class IsManagerUser(BasePermission):
    """Права доступа для сотрудника-менеджера."""

    edit_methods = (
        "PUT",
        "PATCH",
        "DELETE",
    )

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True

        if request.user.is_staff and request.method not in self.edit_methods:
            return True

        return False
