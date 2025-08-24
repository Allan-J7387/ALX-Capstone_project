from rest_framework import permissions

class IsOwnerOrDispatcher(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.role in ("DISPATCHER","ADMIN"):
            return True
        return obj.requester == request.user
