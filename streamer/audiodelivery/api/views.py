from rest_framework.generics import ListAPIView

from audiodelivery.models.getter import get_audio_model

from audiodelivery.api.getter import get_audio_serializer

from audiodelivery.api.permissions import CanRetrieveAudio


class ListAudioView(ListAPIView):
    permission_classes = [CanRetrieveAudio]

    queryset = get_audio_model().objects.all()

    serializer_class = get_audio_serializer()