from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from domain.user.selectors import user_get
from support.utils import get_tokens_for_user
from django.conf import settings
from django.test import tag
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group


User = get_user_model()


class UserDeleteApiTests(APITestCase):
    fixtures = ["fixtures/db_test.json"]

    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()
        cls.user_delete_url = lambda pk: reverse("api:user:delete", args=[pk])

        cls.auth_user_admin = user_get(user_id=1)
        tokens = get_tokens_for_user(cls.auth_user_admin)
        cls.auth_headers_admin = {
            "HTTP_AUTHORIZATION": f"{settings.SIMPLE_JWT['AUTH_HEADER_TYPES']} {tokens['access']}"
        }

        group = Group.objects.first()
        cls.user_to_delete = User.objects.create_user(
            name="Usuário a ser deletado",
            email="delete@teste.com",
            password="senha123",
            group=group,
            is_active=True,
        )

    @tag("unit")
    def test_user_delete(self):
        response = self.client.delete(
            path=self.user_delete_url(self.user_to_delete.id), **self.auth_headers_admin
        )
        self.assertEqual(200, response.status_code)
