from django.conf import settings

from django.apps import apps


DEFAULTS = {
    "chunk": "audiodelivery.AudioChunk",
    "audio": "audiodelivery.Audio"
}

base_var = "AUDIODELIVERY_%(class)s_MODEL"

VARIABLES = {
    "chunk": base_var % {"class": "chunk"},
    "audio": base_var % {"class": "audio"} 
}

def get_model(typo):

    var = VARIABLES[typo]
    default = DEFAULTS[typo]

    model_path = getattr(settings, var, default)

    app_label, model_name = model_path.split(".")

    return apps.get_model(
        app_label=app_label,
        model_name=model_name,
        require_ready=False
    )

def get_audio_model():
    return get_model("audio")

def get_chunk_model():
    return get_model("chunk")