from rest_framework import serializers

from audiodelivery.models.getter import get_audio_model, get_chunk_model

from audiodelivery.api.getter import get_chunk_serializer

from audiodelivery.utils.time import TimeToMillisField


class BaseAudioChunkSerializer(serializers.ModelSerializer):

    start_time = TimeToMillisField()
    end_time = TimeToMillisField()

    class Meta:
        abstract = True


class AudioChunkSerializer(BaseAudioChunkSerializer):
    class Meta:
        model = get_chunk_model()
        fields = ("order", "start_time", "end_time", )


class BaseAudioSerializer(serializers.ModelSerializer):

    chunks = get_chunk_serializer()(many=True)

    class Meta:
        abstract = True

class AudioSerializer(BaseAudioSerializer):
    class Meta:
        model = get_audio_model()
        fields = ("id", "name", "chunks")