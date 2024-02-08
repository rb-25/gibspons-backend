from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.role in ['admin','owner']
class IsOwner(BasePermission):
    def has_permission(self, request, view):
        return request.user.role =='owner'