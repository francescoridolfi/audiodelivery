from django.conf import settings

import sys

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

def is_making_migrations():
    if len(sys.argv) <= 1:
        return False
    
    if sys.argv[1] not in ["makemigrations", "migrate"]:
        return False
    
    return True

def get_model(typo):

    var = VARIABLES[typo]
    default = DEFAULTS[typo]

    model_path = getattr(settings, var, default)

    if is_making_migrations():
        return model_path

    app_label, model_name = model_path.split(".")

    return apps.get_model(
        app_label=app_label,
        model_name=model_name
    )

def get_audio_model():
    return get_model("audio")

def get_chunk_model():
    return get_model("chunk")