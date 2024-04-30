from rest_framework.permissions import BasePermission


class IsModerator(BasePermission):
    message = "Вы не являетесь модератором"

    def has_permission(self, request, view):
        if request.user.groups.filter(name="moderator").exists():
            return True
        return False


class IsOwner(BasePermission):
    message = "Вы не являетесь владельцем!"

    def has_object_permission(self, request, view, obj):
        return request.user == obj.owner
