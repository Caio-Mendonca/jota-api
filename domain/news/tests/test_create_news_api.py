import os.path

from domain.vertical.models import Vertical

PROJECT_ROOT = os.path.dirname(os.path.realpath(__name__))

from domain.file.actions import file_create
from domain.user.selectors import user_get
from support.utils import get_tokens_for_user
from django.test import tag
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from django.conf import settings
from io import BytesIO

from django.core.files.uploadedfile import InMemoryUploadedFile

class NewsCreateApiTests(APITestCase):
    fixtures = [PROJECT_ROOT + "/fixtures/db_test.json"]

    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()

        cls.news_create_url = reverse("api:news:create")

        cls.auth_user_admin = user_get(user_id=1)
        tokens = get_tokens_for_user(cls.auth_user_admin)
        access_admin = tokens["access"]
        cls.auth_headers_admin = {
            "HTTP_AUTHORIZATION": f"{settings.SIMPLE_JWT['AUTH_HEADER_TYPES']} {access_admin}"
        }
        
        cls.auth_user_editor = user_get(user_id=4)
        tokens = get_tokens_for_user(cls.auth_user_editor)
        access_editor = tokens["access"]
        cls.auth_headers_editor = {
            "HTTP_AUTHORIZATION": f"{settings.SIMPLE_JWT['AUTH_HEADER_TYPES']} {access_editor}"
        }

        cls.auth_user_reader = user_get(user_id=6)
        tokens = get_tokens_for_user(cls.auth_user_reader)
        access_reader = tokens["access"]
        cls.auth_headers_reader = {
            "HTTP_AUTHORIZATION": f"{settings.SIMPLE_JWT['AUTH_HEADER_TYPES']} {access_reader}"
        }
    def setUp(self) -> None:
        self.vertical = Vertical.objects.create(name="Vertical Teste")

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
    def test_create_news_as_admin(self):
        data = {
            "title": "Notícia Teste Admin",
            "subtitle": "Subtitulo",
            "content": "Conteúdo da notícia",
            "status": "draft",
            "access_pro": False,
            "image": self.files[0].id,
            "author": 1,
            "vertical": 1,
        }

        response = self.client.post(
            path=self.news_create_url,
            data=data,
            format="json",
            **self.auth_headers_admin,
        )

        self.assertEqual(response.status_code, 201)

    @tag("unit")
    def test_create_news_as_editor(self):
        data = {
            "title": "Notícia Teste Editor",
            "subtitle": "Subtitulo",
            "content": "Conteúdo da notícia",
            "status": "draft",
            "access_pro": False,
            "author": 4,
            "vertical": self.vertical.id,
        }
        print(self.auth_user_editor)
        response = self.client.post(
            path=self.news_create_url,
            data=data,
            format="json",
            **self.auth_headers_editor,
        )

        self.assertEqual(response.status_code, 201)

    @tag("unit")
    def test_create_news_as_reader_should_fail(self):
        data = {
            "title": "Notícia Teste Reader",
            "subtitle": "Subtitulo",
            "content": "Conteúdo da notícia",
            "status": "draft",
            "access_pro": False,
            "author": 3,
            "vertical": self.vertical.id,
        }

        response = self.client.post(
            path=self.news_create_url,
            data=data,
            format="json",
            **self.auth_headers_reader,
        )

        self.assertEqual(response.status_code, 403)
