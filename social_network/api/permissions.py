from rest_framework import permissions
from .models import Like


class IsOwnerOfPost(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            return obj.author.id == request.user.id
        