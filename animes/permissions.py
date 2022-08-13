from rest_framework import permissions


class IsOwnerOrAdmin(permissions.BasePermission):
    message = 'You Can\'t Edit or Delete this Data'

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (obj.user == request.user and request.user.is_staff == True) or request.user.is_superuser == True


class IsPostMethod(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method.upper() == 'POST'

class IsSafeMethod(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method.upper() in ('OPTIONS', 'HEAD', 'GET')

class IsAllowedToAdd(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff == True or request.user.is_superuser == True
