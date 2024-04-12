from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.role in ['admin','owner']
    
class IsCompanyCreator(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user_id == request.user
    
class IsPOCCreater(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.company.user_id == request.user

class IsApproved(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_approved == True