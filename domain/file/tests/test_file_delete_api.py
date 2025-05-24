from io import BytesIO
import os.path
from domain.user.selectors import user_get
from support.utils import get_tokens_for_user

PROJECT_ROOT = os.path.dirname(os.path.realpath(__name__))

from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.test import TestCase, tag
from django.urls import reverse
from unittest.mock import patch

from rest_framework.test import APIClient

from domain.file.actions import file_create


class FileDeleteApiTests(TestCase):
    fixtures = [PROJECT_ROOT + "/fixtures/db_test.json"]

    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()
        cls.auth_user_admin = user_get(user_id=1)
        tokens = get_tokens_for_user(cls.auth_user_admin)
        access_auth_user_admin = tokens["access"]
        cls.auth_headers_user_admin = {
            "HTTP_AUTHORIZATION": f"{settings.SIMPLE_JWT['AUTH_HEADER_TYPES']} {access_auth_user_admin}"
        }


    def setUp(self) -> None:
        new_files = [
            {
                "path": InMemoryUploadedFile(
                    file=BytesIO(b"some dummy bcode data: \x02\x03"),
                    field_name="path",
                    size=28,
                    charset="",
                    name="file1.jpg",
                    content_type="image/jpg",
                ),
                "type_file": "image",
            },
            {
                "path": InMemoryUploadedFile(
                    file=BytesIO(b"some dummy bcode data: \x02\x03"),
                    field_name="path",
                    size=28,
                    charset="",
                    name="file1.jpg",
                    content_type="image/jpg",
                ),
                "type_file": "image",
            },
            {
                "path": InMemoryUploadedFile(
                    file=BytesIO(b"some dummy bcode data: \x02\x03"),
                    field_name="path",
                    size=28,
                    charset="",
                    name="file1.jpg",
                    content_type="image/jpg",
                ),
                "type_file": "image",
            },
        ]

        self.files = [file_create(**file) for file in new_files]

    @tag("unit")
    def test_delete_file(self):
        response = self.client.delete(
            path=reverse("api:files:delete", kwargs={"pk": self.files[2].id}),
            **self.auth_headers_user_admin,
        )

        self.assertEqual(204, response.status_code)