from rest_framework import permissions


class IsUserOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user == obj.user


class IsBuyer(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.user.unlocked_correcs.filter(id=obj.id).exists()
