from rest_framework import permissions


class RestaurantPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.user.rank_type == 'CONFIRM':
            return True
        else:
            return obj.group.id == request.user.group.id
        return False