from rest_framework import permissions


class IsSuperuserOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user.is_superuser

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user.is_superuser


class IsSuperuserOrIsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user == obj.teacher:
            return True

        return request.user.is_superuser
