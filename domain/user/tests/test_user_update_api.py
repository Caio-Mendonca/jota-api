from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from domain.user.selectors import user_get
from support.utils import get_tokens_for_user
from django.conf import settings
from django.test import tag


class UserUpdateApiTests(APITestCase):
    fixtures = ["fixtures/db_test.json"]

    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()
        cls.user_update_url = lambda pk: reverse("api:user:update", args=[pk])

        cls.auth_user_admin = user_get(user_id=1)
        tokens = get_tokens_for_user(cls.auth_user_admin)
        cls.auth_headers_admin = {
            "HTTP_AUTHORIZATION": f"{settings.SIMPLE_JWT['AUTH_HEADER_TYPES']} {tokens['access']}"
        }

    @tag("unit")
    def test_user_update(self):
        user_id = 2
        update_data = {"name": "Usuário Editado", "is_active": False}

        response = self.client.patch(
            path=self.user_update_url(user_id),
            data=update_data,
            format="json",
            **self.auth_headers_admin,
        )

        self.assertEqual(200, response.status_code)
        self.assertEqual(response.data["name"], "Usuário Editado")
        self.assertFalse(response.data["is_active"])
