from rest_framework import permissions
from django.contrib.auth.models import Group

class IsManagerOrAdmin(permissions.BasePermission):
    """
    Custom permission for managers and admins only.
    """
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        
        if request.user.is_authenticated:
            manager_group = Group.objects.filter(name='Manager').first()
            if manager_group and manager_group in request.user.groups.all():
                return True
        
        return False

class IsDeliveryCrewOrManager(permissions.BasePermission):
    """
    Custom permission for delivery crew and managers.
    """
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        
        if request.user.is_authenticated:
            manager_group = Group.objects.filter(name='Manager').first()
            delivery_group = Group.objects.filter(name='Delivery crew').first()
            
            user_groups = request.user.groups.all()
            
            if manager_group and manager_group in user_groups:
                return True
            if delivery_group and delivery_group in user_groups:
                return True
        
        return False

class IsCustomerOrReadOnly(permissions.BasePermission):
    """
    Custom permission for customers - read-only for unauthenticated users.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return request.user.is_authenticated

class IsOwnerOrManager(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object or managers to access it.
    """
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        
        # Check if user is manager
        manager_group = Group.objects.filter(name='Manager').first()
        if manager_group and manager_group in request.user.groups.all():
            return True
        
        # Check if user owns the object
        if hasattr(obj, 'user'):
            return obj.user == request.user
        
        return False
