from rest_framework import permissions

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'ADMIN'

class IsBranchManager(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated
        #and request.user.role in ['ADMIN', 'BRANCH_MANAGER']

class IsRecoverySupervisor(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['ADMIN', 'RECOVERY_SUPERVISOR', 'BRANCH_MANAGER']

class IsCollector(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated
        #and request.user.role in ['ADMIN', 'RECOVERY_SUPERVISOR', 'COLLECTOR']

class IsAuditor(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['ADMIN', 'AUDITOR']


# Combined permissions for different actions
class RecoveryCasePermission(permissions.BasePermission):
    """Custom permission for Recovery Cases"""
    
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
            
        if request.method in permissions.SAFE_METHODS:  # GET, HEAD, OPTIONS
            return True  # All authenticated users can view
            
        # Only collectors, supervisors and above can create/update
        return request.user.role in ['ADMIN', 'RECOVERY_SUPERVISOR', 'COLLECTOR', 'BRANCH_MANAGER']