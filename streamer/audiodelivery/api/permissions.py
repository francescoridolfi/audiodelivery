from django.contrib.auth.models import Permission

from django.http.request import HttpRequest

from rest_framework.permissions import BasePermission

from audiodelivery.models.audio import PERMISSIONS


class BaseAudioDeliveryPermission(BasePermission):

    permission_type = None

    def has_permission(self, request: HttpRequest, view):
        
        if self.permission_type in (None, ""):
            return True

        if self.permission_type not in PERMISSIONS:
            return True
        
        if not request.user.is_authenticated:
            return False

        permission_code = PERMISSIONS[self.permission_type][0]

        perm = Permission.objects.get(codename=permission_code)

        return request.user.has_perm(perm)


class CanRetrieveAudio(BaseAudioDeliveryPermission):
    permission_type = "retrieve"


class CanUploadAudio(BaseAudioDeliveryPermission):
    permission_type = "upload"