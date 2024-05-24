from django.core.files.base import File, ContentFile

from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from audiodelivery.settings import CHUNK_PATH, MAX_CHUNK_DURATION

from audiodelivery.models.getter import get_chunk_model

from pydub import AudioSegment
from io import BytesIO


def get_slots(duration: int, chunk_length: int):

    chunks = (duration + chunk_length - 1) // chunk_length
    
    return [(i*chunk_length, min((i+1)*chunk_length - 1, duration)) for i in range(chunks)]


def splitter(
        file: File,
        populate_model_method,
        storage_method
    ):
    """
    Here is the method that allows splitting an audio file into multiple chunks while managing the saving and creation of the model instance using external methods.

    Args:
        file: this is the input file from the form, it should be a django.core.files.base.File instance or subinstance
        populate_model_method: function that assembles the model instance using the inputs from the current method
        storage_method: a proxy that saves the ContentFile to the correct path using whichever storage the backend specifies
    
    Returns:
        A Queryset with all chunks generated
    """    

    file_format = file.name.split(".")[-1]

    slug_name = slugify(file.name)

    audio = AudioSegment.from_file(file, format=file_format)

    duration = len(audio)

    chunk_ids = []
    chunk_order = 0

    for slot in get_slots(duration, MAX_CHUNK_DURATION):
        start = slot[0]
        end = slot[1]

        chunk = audio[start:end]

        chunk_io = BytesIO()
        chunk.export(chunk_io, format=file_format)
        chunk_io.seek(0)

        path = storage_method(
            output_path=CHUNK_PATH / slug_name,
            filename=f"chunk_{chunk_order}.mp3",
            content=ContentFile(chunk_io.read())
        )

        if path is None:
            raise Exception(_("The file path cannot be null"))

        chunk_model = populate_model_method(
            order=chunk_order,
            start=start,
            end=end,
            path=path,
        )

        if chunk_model is None:
            raise Exception(_("The Model Instance cannot be null"))

        chunk_ids.append(chunk_model.id)

        chunk_order += 1
    
    return get_chunk_model().objects.filter(id__in=chunk_ids)

        

    
