from .models import File


def file_get(*, file_id: int):
    file = File.objects.get(id=file_id)

    return file