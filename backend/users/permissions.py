from rest_framework import permissions


class IsAdminOrIsSelf(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        is_admin = request.user and request.user.is_staff
        is_self = request.user and obj == request.user
        return is_admin or is_self


class IsSelf(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user and obj == request.user

