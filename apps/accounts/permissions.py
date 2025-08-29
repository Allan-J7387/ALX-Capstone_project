class IsDriver(permissions.BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, 'driver_profile')
