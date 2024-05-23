from django.apps import apps

from audiodelivery.settings import MODELS


def get_model(typo):
    model_path = MODELS[typo]

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