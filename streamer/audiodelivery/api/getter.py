from django.utils.translation import gettext_lazy as _

from audiodelivery.settings import SERIALIZERS

import importlib


def import_class_from_string(path_string: str):
    module_name, class_name = path_string.rsplit(".", 1)
    
    module = importlib.import_module(module_name)
    
    return getattr(module, class_name, None)


def get_serializer(typo):
    serializer_path = SERIALIZERS[typo]

    serializer = import_class_from_string(serializer_path)

    if serializer is None:
        raise ModuleNotFoundError(_("Module %(path)s not found") % {"path": serializer_path})

    return serializer


def get_audio_serializer():
    return get_serializer("audio")

def get_chunk_serializer():
    return get_serializer("chunk")