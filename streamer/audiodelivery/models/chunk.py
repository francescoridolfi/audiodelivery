from django.db import models

from django.utils.translation import gettext_lazy as _

from audiodelivery.models.base import BaseModel
from audiodelivery.models.getter import get_audio_model

from audiodelivery.utils.time import convert_to_millis

from audiodelivery.settings import CHUNK_PATH



class BaseAudioChunk(BaseModel):
    class Meta:
        abstract = True

    order = models.PositiveIntegerField(
        _("Order N."),
        default=0,
        help_text=_("Chunk Ordering Number assigned by system while uploading")
    )

    start_time = models.TimeField(
        _("Start Time"),
        help_text=_("Start time of the audio chunk")
    )

    end_time = models.TimeField(
        _("End Time"),
        help_text=_("End time of the audio chunk")
    )

    file_path = models.FilePathField(
        verbose_name=_("File path"),
        path=CHUNK_PATH,
        max_length=255,
        null=True,
        blank=True,
        help_text=_("Path where the file is stored")
    )

    def __str__(self) -> str:
        return f"Chunk n. {self.order} (ID: {self.id})"

    @property
    def parent(self):
        query = get_audio_model().objects.filter(chunks__id=self.id)

        if query.count() == 0:
            return None
        
        return query.first()

    def to_json(self):
        return {
            "order": self.order,
            "start_time": convert_to_millis(self.start_time),
            "end_time": convert_to_millis(self.end_time)
        }

class AudioChunk(BaseAudioChunk):
    class Meta:
        verbose_name = _("Audio Chunk")
        verbose_name_plural = _("Audio Chunks")
