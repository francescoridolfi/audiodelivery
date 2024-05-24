from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.parsers import FileUploadParser

from django.shortcuts import get_object_or_404

from audiodelivery.models.getter import get_audio_model

from audiodelivery.api import get_audio_serializer

from audiodelivery.api.permissions import CanRetrieveAudio, CanUploadAudio

from audiodelivery.backend import get_uplader_backend


class AudioViewSet(ViewSet):
    parser_classes = [FileUploadParser]

    queryset = get_audio_model().objects.all()

    serializer_class = get_audio_serializer()

    def get_permissions(self):
        if self.action in ("list", "retrieve"):
            return [CanRetrieveAudio()]
        
        if self.action in ("create", ):
            return [CanUploadAudio()]
        
        return super(AudioViewSet, self).get_permissions()

    def list(self, request):
        serializer = self.serializer_class(self.queryset, many=True)

        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        audio_instance = get_object_or_404(self.queryset, pk=pk)

        serializer = self.serializer_class(audio_instance)

        return Response(serializer.data)
    
    def create(self, request):
        
        file = request.FILES.get("file")
        
        backend = get_uplader_backend()(file)

        backend.is_valid()

        audio_instance = backend.upload()

        serializer = self.serializer_class(audio_instance)

        return Response(serializer.data)
        
