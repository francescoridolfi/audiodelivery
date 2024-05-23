from django.utils.translation import gettext_lazy as _

from django.core.files.base import File
from django.core.exceptions import ValidationError

from audiodelivery.settings import ALLOWED_FORMATS, FILE_VALIDATORS

from audiodelivery.utils.importer import import_module_from_string


class BaseAudioValidator:

    def __call__(self, file: File):
        self.file = file

        return self.validate()

    def validate(self):
        raise NotImplementedError(_("Validator criteria not implemented"))


class AudioFormatValidator(BaseAudioValidator):
    """
    Validator that checks if the audio file complies with the allowed formats.
    """

    def validate(self):
        if not self.file.name.split(".")[-1].lower() in ALLOWED_FORMATS:
            raise ValidationError(_("Unsupported file extension."))

    

def get_file_validators():
    return [import_module_from_string(validator) for validator in FILE_VALIDATORS] + [AudioFormatValidator]