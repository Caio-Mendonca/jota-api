import os.path

PROJECT_ROOT = os.path.dirname(os.path.realpath(__name__))

from domain.user.selectors import user_get
from support.utils import get_tokens_for_user
from django.test import tag
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from django.conf import settings


class UserCreateApiTests(APITestCase):
    fixtures = [PROJECT_ROOT + "/fixtures/db_test.json"]

    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()

        cls.user_create_url = reverse("api:user:create")

        cls.auth_user_admin = user_get(user_id=1)
        tokens = get_tokens_for_user(cls.auth_user_admin)
        access_auth_user_admin = tokens["access"]
        cls.auth_headers_user_admin = {
            "HTTP_AUTHORIZATION": f"{settings.SIMPLE_JWT['AUTH_HEADER_TYPES']} {access_auth_user_admin}"
        }

        cls.auth_user_editor = user_get(user_id=2)
        tokens = get_tokens_for_user(cls.auth_user_editor)
        access_editor = tokens["access"]
        cls.auth_headers_editor = {
            "HTTP_AUTHORIZATION": f"{settings.SIMPLE_JWT['AUTH_HEADER_TYPES']} {access_editor}"
        }

        cls.auth_user_reader = user_get(user_id=3)
        tokens = get_tokens_for_user(cls.auth_user_reader)
        access_reader = tokens["access"]
        cls.auth_headers_reader = {
            "HTTP_AUTHORIZATION": f"{settings.SIMPLE_JWT['AUTH_HEADER_TYPES']} {access_reader}"
        }

    @tag("unit")
    def test_create_user_admin(self):
        new_user = {
            "is_active": True,
            "email": "testeautomatizado@testeautomatizado.com.br",
            "name": " Teste",
            "password": "testeSenha",
            "group": 1,
        }

        response = self.client.post(
            path=self.user_create_url,
            data=new_user,
            format="json",
            **self.auth_headers_user_admin,
        )

        self.assertEqual(201, response.status_code)

    @tag("unit")
    def test_create_user_with_editor(self):
        new_user = {
            "is_active": True,
            "email": "testeautomatizado@testeautomatizado.com.br",
            "name": " Teste",
            "password": "testeSenha",
            "group": 2,
        }

        response = self.client.post(
            path=self.user_create_url,
            data=new_user,
            format="json",
            **self.auth_headers_editor,
        )

        self.assertEqual(201, response.status_code)

    @tag("unit")
    def test_create_user_with_reader(self):
        new_user = {
            "is_active": True,
            "email": "testeautomatizado@testeautomatizado.com.br",
            "name": " Teste",
            "password": "testeSenha",
            "group": 1,
        }

        response = self.client.post(
            path=self.user_create_url,
            data=new_user,
            format="json",
            **self.auth_headers_reader,
        )

        self.assertEqual(201, response.status_code)
