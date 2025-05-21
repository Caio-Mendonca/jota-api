import os.path

PROJECT_ROOT = os.path.dirname(os.path.realpath(__name__))

from django.urls import reverse
from django.conf import settings
from django.test import TestCase, tag

from rest_framework.test import APIClient

from domain.user.selectors import user_get
from support.utils import get_tokens_for_user


class UserMeApiTests(TestCase):
    fixtures = [PROJECT_ROOT + "/fixtures/db_test.json"]

    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()

        cls.me_url = reverse("api:auth:me")

        cls.auth_user = user_get(user_id=1)

        tokens = get_tokens_for_user(cls.auth_user)
        access, cls.refresh = tokens["access"], tokens["refresh"]

        cls.auth_headers = {
            "HTTP_AUTHORIZATION": f"{settings.SIMPLE_JWT['AUTH_HEADER_TYPES']} {access}"
        }

    @tag("unit")
    def test_user_me_authenticated(self):
        response = self.client.get(path=self.me_url, **self.auth_headers)

        self.assertEqual(200, response.status_code)
        self.assertEqual(response.data["id"], self.auth_user.id)
        self.assertEqual(response.data["email"], self.auth_user.email)

    @tag("unit")
    def test_user_me_unauthenticated(self):
        response = self.client.get(path=self.me_url)

        self.assertEqual(401, response.status_code)
