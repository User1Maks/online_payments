from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """Права доступа владельца кошелька."""

    def has_object_permission(self, request, view, obj):
        return request.user == obj.owner
