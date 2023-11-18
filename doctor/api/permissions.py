from rest_framework import permissions


class IsDoctor(permissions.BasePermission):
    """
    Allows access only to doctors users.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_doctor)
