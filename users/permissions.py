from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.email == request.user.email


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff
