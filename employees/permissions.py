from rest_framework import permissions


class EmployeePermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.user.rank_type == 'CONFIRM':
            return True
        else:
            if hasattr(obj, 'id'):
                return obj.id == request.user.id
        return False