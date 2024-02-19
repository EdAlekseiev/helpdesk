from rest_framework.permissions import BasePermission


class IsClientPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_client


class IsOperatorPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_operator
