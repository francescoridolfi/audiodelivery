from django.core.files.base import File, ContentFile
from django.core.files.storage import default_storage

from django.core.exceptions import ValidationError

from django.utils.translation import gettext_lazy as _

from audiodelivery.models.getter import get_chunk_model

from audiodelivery.utils.validators import get_file_validators
from audiodelivery.utils.chunker import splitter
from audiodelivery.utils.time import convert_from_millis


class BaseAudioUploaderBackend:

    file: File = None
    chunks = []

    def __init__(self, file: File) -> None:
        self.file = file

    def validators(self) -> list[any]:
        return []

    def _validators(self):
        if self.validators():
            return self.validators()
        
        return get_file_validators()

    def is_valid(self):
        errors = []

        for validator in self._validators():
            try:
                validator(self.file)
            except ValidationError as ve:
                errors.append(ve)
            except Exception as e:
                errors.append(ValidationError(str(e)))

        if errors:
            raise ValidationError(errors)
        
        return True

    def chunkit(self):
        raise NotImplementedError(_("Chunk Criteria not implemented"))


    def upload(self):
        pass


class DefaultStorageAudioUploaderBackend(BaseAudioUploaderBackend):
    def chunkit(self):

        def chunk_model_generator(
            order: int,
            start: int,
            end: int,
            path
        ):
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
            return default_storage.save(output_path / filename, content)

        return splitter(
            self.file,
            chunk_model_generator,
            save_to_storage
        )