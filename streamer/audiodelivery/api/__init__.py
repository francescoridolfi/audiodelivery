from django.utils.translation import gettext_lazy as _

from audiodelivery.settings import SERIALIZERS

from audiodelivery.utils.importer import import_module_from_string


def get_serializer(typo):
    serializer_path = SERIALIZERS[typo]

    serializer = import_module_from_string(serializer_path)

    if serializer is None:
        raise ModuleNotFoundError(_("Module %(path)s not found") % {"path": serializer_path})

    return serializer


def get_audio_serializer():
    return get_serializer("audio")

def get_chunk_serializer():
    return get_serializer("chunk")