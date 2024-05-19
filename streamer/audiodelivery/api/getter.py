from django.conf import settings


DEFAULTS = {
    "chunk": "audiodelivery.api.serializers.AudioChunkSerializer",
    "audio": "audiodelivery.api.serializers.AudioSerializer"
}

base_var = "AUDIODELIVERY_%(class)s_SERIALIZER"

VARIABLES = {
    "chunk": base_var % {"class": "chunk"},
    "audio": base_var % {"class": "audio"} 
}

def get_serializer(typo):

    var = VARIABLES[typo]
    default = DEFAULTS[typo]

    serializer_path = getattr(settings, var, default)

    class_name = serializer_path.split(".")[-1]
    file_name = "".join(serializer_path.split(".")[:-1])

    pkg = __import__(file_name)
    
    return getattr(pkg, class_name, None)


def get_audio_serializer():
    return get_serializer("audio")

def get_chunk_serializer():
    return get_serializer("chunk")