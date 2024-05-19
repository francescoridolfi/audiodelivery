from django.conf import settings

from django.utils.translation import gettext_lazy as _

from django.core.exceptions import ValidationError

def audio_format_validator(value):
    allowed_formats = getattr(settings, "AUDIODELIVERY_ALLOWED_FORMATS", (".mp3", ))

    if not value.name.split(".")[-1].lower() in allowed_formats:
        raise ValidationError(_("Unsupported file extension."))