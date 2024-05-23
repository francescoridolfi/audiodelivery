from django.conf import settings

from django.utils.translation import gettext_lazy as _

# PERMISSION SETTINGS

PERMISSIONS = getattr(settings, "AUDIODELIVERY_PERMISSIONS", {
    "retrieve": ("can_retrieve", _("Can User retrieve Audio infos")),
    "upload": ("can_upload", _("Can User upload new Audio"))
})

# CHUNK SETTINGS

CHUNK_PATH = getattr(settings, "AUDIODELIVERY_CHUNK_DIR", settings.BASE_DIR / "chunks")

MAX_CHUNK_DURATION = getattr(settings, "AUDIODELIVERY_MAX_CHUNK_DURATION", 9999)

# DB SETTINGS

_model_defaults = {
    "chunk": "audiodelivery.AudioChunk",
    "audio": "audiodelivery.Audio"
}

_model_base_var = "AUDIODELIVERY_%(class)s_MODEL"

_model_variables = {
    "chunk": _model_base_var % {"class": "chunk"},
    "audio": _model_base_var % {"class": "audio"} 
}

MODELS = {
    "chunk": getattr(settings, _model_variables["chunk"], _model_defaults["chunk"]),
    "audio": getattr(settings, _model_variables["audio"], _model_defaults["audio"])
}

# API SETTINGS

_serializer_defaults = {
    "chunk": "audiodelivery.api.serializers.AudioChunkSerializer",
    "audio": "audiodelivery.api.serializers.AudioSerializer"
}

_serializer_base_var = "AUDIODELIVERY_%(class)s_SERIALIZER"

_serializer_variables = {
    "chunk": _serializer_base_var % {"class": "chunk"},
    "audio": _serializer_base_var % {"class": "audio"} 
}

SERIALIZERS = {
    "chunk": getattr(settings, _serializer_variables["chunk"], _serializer_defaults["chunk"]),
    "audio": getattr(settings, _serializer_variables["audio"], _serializer_defaults["audio"])
}

# VALIDATORS SETTINGS

ALLOWED_FORMATS = getattr(settings, "AUDIODELIVERY_ALLOWED_FORMATS", ("mp3", ))

FILE_VALIDATORS = getattr(settings, "AUDIODELIVERY_UPLOAD_VALIDATORS", [])


