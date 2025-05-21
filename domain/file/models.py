from django.db import models

from support.models import BaseModel
from .exceptions import InvalidAttachmentFormat, InvalidImageFormat


class File(BaseModel):
    class Meta:
        db_table = "file"
        ordering = ["created_at"]

    class TypeFile(models.TextChoices):
        IMAGE = "image", "Imagem"
        ATTACHMENT = "attachment", "Anexo"

    path = models.FileField(upload_to="uploads/")
    type_file = models.CharField(
        choices=TypeFile.choices, db_index=True, max_length=100
    )

    def clean(self):
        if (
            self.type_file == "attachment"
            and not self.check_file_is_valid_attachment_format(
                type_file=self.path.file.content_type
            )
        ):
            raise InvalidAttachmentFormat()

        if self.type_file == "image" and not self.check_file_is_valid_image_format(
            type_file=self.path.file.content_type
        ):
            raise InvalidImageFormat()

    @staticmethod
    def check_file_is_valid_image_format(
        type_file: str,
    ) -> bool:
        if not (
            type_file == "image/png"
            or type_file == "image/jpeg"
            or type_file == "image/jpg"
            or type_file == "image/gif"
            or type_file == "image/webp"
        ):
            return False
        return True

    @staticmethod
    def check_file_is_valid_attachment_format(
        type_file: str,
    ) -> bool:
        if not (
            type_file
            == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            or type_file == "application/vnd.ms-excel"
        ):
            return False
        return True

    def __str__(self):
        return f"type={self.type_file}, url={self.path}"