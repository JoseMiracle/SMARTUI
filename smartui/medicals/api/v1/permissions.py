from rest_framework.permissions import BasePermission
from django.contrib.auth import get_user_model
from smartui.medicals.models import ExternalProviderStaff

User = get_user_model()


class IsDoctor(BasePermission):

    """
        Permission to block non-doctor 
    """
    message = "You aren't a doctor"

    def has_permission(self, request, view):
        user = User.objects.filter(id=request.user.id).first()
        if user.role == 'doctor':
            return True
        else:
            False

class IsAdmin(BasePermission):

    """
        Permssion to admin roles like adding externl provide
    """
    message = "You are not an admin"

    def has_permission(self, request, view):
        user = User.objects.filter(id=request.user.id).first()
        if user.is_superuser:
            return True
        else:
            return False

        return super().has_permission(request, view)

class IsDoctorOrExternalProvider(BasePermission):
    """
        Permission for doctor or external providers
    """
    message = 'You are not a doctor or External provider staff'

    def has_permission(self, request, view):
        user = User.objects.filter(id=request.user.id).first()
        external_provider_staff = ExternalProviderStaff.objects.filter(staff=user).first()

        if user.role == 'doctor' or external_provider_staff is not None:
            return True
        else:
            return False
        

# class BlocklistPermission(permissions.BasePermission):
#     """
#     Global permission check for blocked IPs.
#     """

#     def has_permission(self, request, view):
#         ip_addr = request.META['REMOTE_ADDR']
#         blocked = Blocklist.objects.filter(ip_addr=ip_addr).exists()
#         return not blocked