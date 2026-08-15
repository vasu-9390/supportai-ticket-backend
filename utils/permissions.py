from rest_framework import permissions

class IsAdminUserRole(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and (request.user.role == 'Admin' or request.user.is_staff or request.user.is_superuser)

class IsAgentUserRole(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and (request.user.role in ['Agent', 'Admin'] or request.user.is_staff)

class IsCustomerUserRole(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

class IsOwnerOrAgentOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.user.role in ['Admin', 'Agent'] or request.user.is_staff:
            return True
        # Check if customer or author
        if hasattr(obj, 'customer') and hasattr(obj.customer, 'email'):
            return obj.customer.email == request.user.email
        if hasattr(obj, 'email'):
            return obj.email == request.user.email
        if hasattr(obj, 'user'):
            return obj.user == request.user
        return False
