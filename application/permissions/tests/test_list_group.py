import os.path

PROJECT_ROOT = os.path.dirname(os.path.realpath(__name__))

from django.urls import reverse
from django.conf import settings
from django.test import TestCase, tag

from rest_framework.test import APIClient

from domain.user.selectors import user_get
from support.utils import get_tokens_for_user


class GroupListApiTests(TestCase):
    fixtures = [PROJECT_ROOT + "/fixtures/db_test.json"]

    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()

        cls.group_list_url = reverse("api:groups:list")

        cls.auth_user = user_get(user_id=1)

        tokens = get_tokens_for_user(cls.auth_user)
        access, cls.refresh = tokens["access"], tokens["refresh"]

        cls.auth_headers = {
            "HTTP_AUTHORIZATION": f"{settings.SIMPLE_JWT['AUTH_HEADER_TYPES']} {access}"
        }

    @tag("unit")
    def test_group_list_authenticated(self):
        response = self.client.get(path=self.group_list_url, **self.auth_headers)

        self.assertEqual(200, response.status_code)
        self.assertIn("groups", response.data)

    @tag("unit")
    def test_group_list_unauthenticated(self):
        response = self.client.get(path=self.group_list_url)

        self.assertEqual(401, response.status_code)
