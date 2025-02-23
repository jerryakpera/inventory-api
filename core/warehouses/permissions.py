"""
Permission definitions for the warehouse app.
"""

from rest_framework import permissions

from .models import WarehouseUser


class IsWarehouseManagerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow only warehouse managers to modify warehouse data.
    """

    def has_permission(self, request, view):
        """
        Check if the user has permission to perform the action.

        Parameters
        ----------
        request : Request
            The current request instance.
        view : View
            The view being accessed.

        Returns
        -------
        bool
            True if the user has permission, False otherwise.
        """
        # Allow read-only permissions for GET, HEAD, and OPTIONS requests
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """
        Check if the user has permission to perform actions on a specific object.

        Parameters
        ----------
        request : Request
            The current request instance.
        view : View
            The view being accessed.
        obj : Warehouse
            The warehouse instance being modified.

        Returns
        -------
        bool
            True if the user has the required permissions, False otherwise.
        """
        if request.method in permissions.SAFE_METHODS:
            return True

        # Check if the user is assigned as a MANAGER in the warehouse
        return WarehouseUser.objects.filter(
            user=request.user,
            warehouse=obj,
            role=WarehouseUser.RoleChoices.MANAGER,
        ).exists()
