from rest_framework.permissions import BasePermission

class IsSuperUser(BasePermission):

    """
    Allows access to superusers.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_superuser
    
class IsAdmin(BasePermission):
    """
    Allows access to admin.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'ADMIN'
    
class IsUser(BasePermission):
    """
    Allows access to Organizer Events.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'USER'
    
class IsAdminOrSuperUser(BasePermission):
    """
    Allows access to admin and superusers.
    """
    def has_permission(self, request, view):
        return (
            request.user and request.user.is_authenticated and (
                request.user.is_superuser or request.user.role == 'ADMIN'
            )
        )