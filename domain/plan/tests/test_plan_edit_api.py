import os.path

PROJECT_ROOT = os.path.dirname(os.path.realpath(__name__))

from domain.plan.actions import plan_create
from domain.user.selectors import user_get
from support.utils import get_tokens_for_user
from django.test import tag
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from django.conf import settings


class PlanEditApiTests(APITestCase):
    fixtures = [PROJECT_ROOT + "/fixtures/db_test.json"]

    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()

        cls.plan_edit_url = lambda pk: reverse("api:plan:edit", kwargs={"pk": pk})

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
    def setUp(self) -> None:
        new_plan = {
            "name": "Plano Avançado",
            "description": "Plano de testes para leitores",
        }

        self.plan = plan_create(
            name=new_plan["name"],
            description=new_plan["description"],
            created_by=self.auth_user_admin,
        )


    @tag("unit")
    def test_edit_plan_admin(self):
        update_plan_data = {
            "name": "Plano Atualizado",
        }

        pk = self.plan.pk
        response = self.client.patch(
            path=self.plan_edit_url(pk),
            data=update_plan_data,
            format="json",
            **self.auth_headers_user_admin,
        )

        self.assertEqual(200, response.status_code)
        self.assertEqual(response.data["name"], update_plan_data["name"])

    @tag("unit")
    def test_edit_plan_editor_forbidden(self):
        update_plan_data = {
            "name": "Plano Editor",
        }

        pk = 1
        response = self.client.patch(
            path=self.plan_edit_url(pk),
            data=update_plan_data,
            format="json",
            **self.auth_headers_editor,
        )

        self.assertEqual(403, response.status_code)

    @tag("unit")
    def test_edit_plan_reader_forbidden(self):
        update_plan_data = {
            "name": "Plano Reader",
        }

        pk = 1
        response = self.client.patch(
            path=self.plan_edit_url(pk),
            data=update_plan_data,
            format="json",
            **self.auth_headers_reader,
        )

        self.assertEqual(403, response.status_code)
