from rest_framework import permissions


class EmployeePermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.user.rank_type == 'CONFIRM':
                return True
            else:
                return False
        else:
            return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
                if hasattr(obj, 'id'):
                    return obj.id == request.user.id
                else:
                    return False
        return False