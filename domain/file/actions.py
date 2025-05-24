from .models import File
from django.core.files.uploadedfile import InMemoryUploadedFile

from support.actions import model_update


def file_create(*, path: InMemoryUploadedFile, type_file: str) -> File:
    file = File(path=path, type_file=type_file)

    file.full_clean()
    file.save()

    return file


def file_update(*, file: File, data) -> File:
    non_side_effect_fields = ["path"]

    file, has_updated = model_update(
        instance=file, fields=non_side_effect_fields, data=data
    )

    return file