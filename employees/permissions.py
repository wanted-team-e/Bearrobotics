from rest_framework import permissions


class EmployeePermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
                if hasattr(obj, 'id'):
                    return obj.id == request.user.id
                else:
                    return False
        return False