from django.db import models

from django.conf import settings

from django.utils.translation import gettext_lazy as _

from audiodelivery.models.base import BaseModel
from audiodelivery.models.getter import get_chunk_model

PERMISSIONS = getattr(settings, "AUDIODELIVERY_PERMISSIONS", {
    "retrieve": ("can_retrieve", _("Can User retrieve Audio infos")),
    "upload": ("can_upload", _("Can User upload new Audio"))
})


class BaseAudio(BaseModel):
    class Meta:
        abstract = True

    name = models.CharField(
        _("Name"),
        max_length=255,
        unique=True,
    )

    chunks = models.ManyToManyField(
        get_chunk_model(),
        verbose_name=_("Audio Chunks")
    )

    def __str__(self) -> str:
        return self.name
    
    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "chunks": [chunk.to_json() for chunk in self.chunks.all()]
        }


class Audio(BaseAudio):
    class Meta:
        verbose_name = _("Audio")
        verbose_name_plural = _("Audios")

        permissions = list()

        if "retrieve" in PERMISSIONS:
            permissions.append(PERMISSIONS["retrieve"])
        
        if "upload" in PERMISSIONS:
            permissions.append(PERMISSIONS["upload"])

        permissions = tuple(permissions)