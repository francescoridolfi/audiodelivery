from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

from audiodelivery.models.getter import get_chunk_model

from audiodelivery.backend.base import BaseAudioUploaderBackend

from audiodelivery.utils.chunker import splitter
from audiodelivery.utils.time import convert_from_millis


class DefaultStorageAudioUploaderBackend(BaseAudioUploaderBackend):
    """
    This backend handles the chunking process using the default chunk model for saving to the database,
    and the default storage for saving chunks in the storage.

    Examples:
        # Initialize the backend passing the django.core.files.base.File object:\n
        backend = DefaultStorageAudioUploaderBackend(uploaded_file)
        
        # Check for validations:\n
        backend.is_valid()

        # Get the audio model:\n
        audio_instance = backend.upload()
    """


    def chunkit(self):
        """Chunk the file and save the chunks to storage."""

        def chunk_model_generator(
            order: int,
            start: int,
            end: int,
            path
        ):
            """Generate a chunk model instance."""
            return get_chunk_model().objects.create(
                order=order,
                start_time=convert_from_millis(start),
                end_time=convert_from_millis(end),
                file_path=path
            )

        def save_to_storage(
            output_path: str,
            filename: str,
            content: ContentFile
        ):
            """Save the chunk to the default storage."""
            import os

            if not os.path.exists(output_path):
                os.mkdir(output_path)
            
            return default_storage.save(output_path / filename, content)

        return splitter(
            self.file,
            chunk_model_generator,
            save_to_storage
        )