from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from domain.user.selectors import user_get
from support.utils import get_tokens_for_user
from django.conf import settings
from django.test import tag


class UserListApiTests(APITestCase):
    fixtures = ["fixtures/db_test.json"]

    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()
        cls.user_list_url = reverse("api:user:list")

        cls.auth_user_admin = user_get(user_id=1)
        tokens = get_tokens_for_user(cls.auth_user_admin)
        cls.auth_headers_admin = {
            "HTTP_AUTHORIZATION": f"{settings.SIMPLE_JWT['AUTH_HEADER_TYPES']} {tokens['access']}"
        }

    @tag("unit")
    def test_user_list(self):
        response = self.client.get(path=self.user_list_url, **self.auth_headers_admin)
        self.assertEqual(200, response.status_code)
        self.assertIn("results", response.json())
