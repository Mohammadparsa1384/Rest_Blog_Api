from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAuthorOrAdminOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.author == request.user.profile or request.user.is_staff