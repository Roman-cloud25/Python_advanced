from rest_framework.permissions import BasePermission, SAFE_METHODS

# Custom permission: only the owner can edit or delete.
class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Safe methods (GET, HEAD, OPTIONS) allowed for all
        if request.method in SAFE_METHODS:
            return True

        # Write methods only for the owner
        return obj.owner == request.user