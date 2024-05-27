from django.utils.translation import gettext_lazy as _

from django.core.files.base import File

from rest_framework.exceptions import ValidationError

from audiodelivery.settings import (
    ALLOWED_FORMATS, FILE_VALIDATORS,
    AUDIO_MAX_DURATION, AUDIO_MAX_SIZE
)

from audiodelivery.utils.importer import import_module_from_string

from pydub import AudioSegment


class BaseAudioValidator:

    _cached_audio = None
    name = None

    def __call__(self, file: File):
        self.file = file

        self.validate()

        # IMPORTANT: remember to seek the file to 0.
        self.file.seek(0)
    
    @property
    def audio(self) -> AudioSegment:
        if not self._cached_audio:
            try:
                self._cached_audio = AudioSegment.from_mp3(self.file)
            except:
                raise ValidationError(_("Corrupted file or not an audio type"))

        return self._cached_audio
        
    def throw(self, message: str):
        raise ValidationError(message, code=self.name)

    def validate(self):
        """ Override this method to include your validation criteria """
        raise NotImplementedError(_("Validator criteria not implemented"))


class AudioFormatValidator(BaseAudioValidator):
    """
    Validator that checks if the audio file complies with the allowed formats.
    """

    name = "format-invalid"

    def validate(self):
        if not self.file.name.split(".")[-1].lower() in ALLOWED_FORMATS:
            self.throw(_("Unsupported file extension."))


class AudioMaxSizeValidator(BaseAudioValidator):
    """
    Validator that checks if the audio size complies with the settings
    """

    name = "size-invalid"

    def validate(self):
        if self.file.size > AUDIO_MAX_SIZE:
            self.throw(_("File too large, maximum size allowed: %(size)s MB") % {"size": AUDIO_MAX_SIZE / (1024*1024)})


class AudioMaxLengthValidator(BaseAudioValidator):
    """
    Validator that checks if the audio length complies with the settings
    """

    name = "length-invalid"

    def validate(self):
        if len(self.audio) > AUDIO_MAX_DURATION:
            self.throw(_("Audio too long, maximum available seconds: %(time)s seconds") % {"time": AUDIO_MAX_DURATION / (1000)})

    

def get_default_validators() -> list[BaseAudioValidator]:
    return [
        AudioFormatValidator(),
        AudioMaxSizeValidator(),
        AudioMaxLengthValidator(),
    ]

def get_imported_validators() -> list[BaseAudioValidator]:
    return [
        import_module_from_string(validator)() 
        for validator in FILE_VALIDATORS
        ]

def get_file_validators() -> list[BaseAudioValidator]:
    return get_default_validators() + get_imported_validators()