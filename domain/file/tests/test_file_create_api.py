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


class FileCreateApiTests(TestCase):
    fixtures = [PROJECT_ROOT + "/fixtures/db_test.json"]

    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()

        cls.file_create_url = reverse("api:files:create")
        cls.auth_user_admin = user_get(user_id=1)
        tokens = get_tokens_for_user(cls.auth_user_admin)
        access_auth_user_admin = tokens["access"]
        cls.auth_headers_user_admin = {
            "HTTP_AUTHORIZATION": f"{settings.SIMPLE_JWT['AUTH_HEADER_TYPES']} {access_auth_user_admin}"
        }


    @tag("unit")
    def test_create_image_file(self):
        new_file = InMemoryUploadedFile(
            file=BytesIO(b"some dummy bcode data: \x02\x03"),
            field_name="path",
            size=28,
            charset="",
            name="file1.jpg",
            content_type="image/jpg",
        )

        response = self.client.post(
            path=self.file_create_url,
            data={"path": new_file, "type_file": "image"},
            **self.auth_headers_user_admin,
        )

        self.assertEqual(201, response.status_code)

    @tag("unit")
    def test_create_attachment_file(self):
        new_file = InMemoryUploadedFile(
            file=BytesIO(b"some dummy bcode data: \x02\x03"),
            field_name="path",
            size=28,
            charset="",
            name="file1.xlsx",
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )

        response = self.client.post(
            path=self.file_create_url,
            data={"path": new_file, "type_file": "attachment"},
            **self.auth_headers_user_admin,
        )

        self.assertEqual(201, response.status_code)

    @tag("unit")
    def test_create_invalid_image_file(self):
        new_file = InMemoryUploadedFile(
            file=BytesIO(
                b"httpsokjdljljs/console\ntest\n9652323.Oi\n\nklsdjlksjlksj\nashjlsjkds\n"
            ),
            field_name="path",
            size=83,
            charset="",
            name="file1.txt",
            content_type="text/plain",
        )

        response = self.client.post(
            path=self.file_create_url,
            data={"path": new_file, "type_file": "image"},
            **self.auth_headers_user_admin,
        )
        self.assertEqual(400, response.status_code)

    @tag("unit")
    def test_create_invalid_attachment_file(self):
        new_file = InMemoryUploadedFile(
            file=BytesIO(
                b"httpsokjdljljs/console\ntest\n9652323.Oi\n\nklsdjlksjlksj\nashjlsjkds\n"
            ),
            field_name="path",
            size=83,
            charset="",
            name="file1.doc",
            content_type="text/plain",
        )

        response = self.client.post(
            path=self.file_create_url,
            data={"path": new_file, "type_file": "attachment"},
            **self.auth_headers_user_admin,
        )
        self.assertEqual(400, response.status_code)