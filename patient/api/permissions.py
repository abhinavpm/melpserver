from rest_framework import permissions
from rest_framework.response import Response


class IsUserOrDoctor(permissions.BasePermission):
    """
    Allows access only to regular users (non-doctor users).
    """

    def has_permission(self, request, view):
        return bool(request.user and (request.user.is_user or request.user.is_doctor))
