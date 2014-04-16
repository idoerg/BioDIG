from rest_framework import permissions

class IsAuthenticatedAndActiveOrReadOnly(permissions.BasePermission):
    '''
        Global permission to allow only active users to perform operations.
    '''

    def has_permission(self, request, view, obj=None):
        return request.method in permissions.SAFE_METHODS or (
            request.user and request.user.is_authenticated() and
            request.user.is_active)
