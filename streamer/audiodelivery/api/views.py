from rest_framework.generics import ListAPIView

from audiodelivery.models.getter import get_audio_model

from audiodelivery.api.getter import get_audio_serializer


class ListAudioView(ListAPIView):
    queryset = get_audio_model().objects.all()

    serializer_class = get_audio_serializer()