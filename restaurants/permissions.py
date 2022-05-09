from rest_framework import permissions


class RestaurantPermission(permissions.BasePermission):

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
            if request.user.rank_type == 'CONFIRM':
                return True
            else:
                return False
        else:
            return False


class GuestInfoPermission(permissions.BasePermission):

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
            if request.user.rank_type == 'CONFIRM':
                return True
            else:
                return False
        else:
            return False
