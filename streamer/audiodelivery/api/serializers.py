from rest_framework import serializers

from audiodelivery.models.getter import get_audio_model, get_chunk_model

from audiodelivery.api.getter import get_chunk_serializer


class BaseAudioChunkSerializer(serializers.ModelSerializer):

    class Meta:
        abstract = True
        fields = ("order", "start_time", "end_time", )


class AudioChunkSerializer(BaseAudioChunkSerializer):
    class Meta:
        model = get_chunk_model()


class BaseAudioSerializer(serializers.ModelSerializer):

    chunks = get_chunk_serializer()(many=True)

    class Meta:
        abstract = True
        fields = ("id", "name")

class AudioSerializer(BaseAudioSerializer):
    class Meta:
        model = get_audio_model()