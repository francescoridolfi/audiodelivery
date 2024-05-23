from django.utils.translation import gettext_lazy as _

from django.core.exceptions import ValidationError

from audiodelivery.settings import ALLOWED_FORMATS


def audio_format_validator(value):

    if not value.name.split(".")[-1].lower() in ALLOWED_FORMATS:
        raise ValidationError(_("Unsupported file extension."))