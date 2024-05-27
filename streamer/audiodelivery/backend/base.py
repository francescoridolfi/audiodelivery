from django.core.files.base import File

from rest_framework.exceptions import ValidationError

from django.utils.translation import gettext_lazy as _

from audiodelivery.models.getter import get_audio_model
from audiodelivery.models import Audio

from audiodelivery.utils.validators import get_file_validators


class BaseAudioUploaderBackend:
    """
    Base Backend that manage validating and chunking functions for an audio file.

    Args:
        file: must be a django.core.files.base.File object

    Methods:
        validators: Override this method to set custom validators.
        is_valid: Call this method to check if the file passes the validation process.
        upload: Returns the audio model stored in the database and loaded with chunks.
        chunkit: Override this method to change the chunk storing and saving criteria.
    """

    file: File = None
    chunks = None
    cached_audio = None

    def __init__(self, file: File) -> None:
        self.file = file

    def validators(self) -> list[any]:
        """Override this method to set custom validators."""
        return []

    def  _validators(self):
        """Get the list of validators, either custom or default."""
        if len(self.validators()) > 0:
            return self.validators()
        
        return get_file_validators()

    def is_valid(self):
        """Check if the file passes the validation process."""
        errors = {}

        for validator in self._validators():
            try:
                validator(self.file)
            except ValidationError as ve:
                errors[ve.get_codes()[0]] = ve.detail
            except Exception as e:
                errors["generic"] = str(e)

        if errors:
            raise ValidationError(errors)
        
        return True

    def chunkit(self):
        """Override this method to define the chunk storing and saving criteria."""
        raise NotImplementedError(_("Chunk Criteria not implemented"))


    def upload(self):
        if self.cached_audio:
            return self.cached_audio
        
        self.chunks = self.chunkit()

        self.cached_audio: Audio = get_audio_model().objects.create(name=self.file.name)
        self.cached_audio.chunks.add(*self.chunks)
        self.cached_audio.save()

        del self.file

        return self.cached_audio


