from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from domain.user.selectors import user_get
from support.utils import get_tokens_for_user
from django.conf import settings
from django.test import tag


class UserDetailApiTests(APITestCase):
    fixtures = ["fixtures/db_test.json"]

    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()
        cls.user_detail_url = lambda pk: reverse("api:user:detail", args=[pk])

        cls.auth_user_admin = user_get(user_id=1)
        tokens = get_tokens_for_user(cls.auth_user_admin)
        cls.auth_headers_admin = {
            "HTTP_AUTHORIZATION": f"{settings.SIMPLE_JWT['AUTH_HEADER_TYPES']} {tokens['access']}"
        }

    @tag("unit")
    def test_user_detail(self):
        user_id = 1
        response = self.client.get(
            path=self.user_detail_url(user_id), **self.auth_headers_admin
        )
        self.assertEqual(200, response.status_code)
        self.assertIn("email", response.json())
