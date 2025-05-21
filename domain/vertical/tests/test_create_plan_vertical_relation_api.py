import os.path

from domain.user.selectors import user_get
from support.utils import get_tokens_for_user
from django.test import tag
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from django.conf import settings
from domain.plan.models import Plan
from domain.vertical.models import Vertical


class PlanVerticalCreateApiTests(APITestCase):
    fixtures = [os.path.dirname(os.path.realpath(__name__)) + "/fixtures/db_test.json"]

    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()

        cls.plan_vertical_create_url = reverse("api:vertical:create_relation")

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
        
        cls.plan = Plan.objects.create(
            name="Plano Teste",
            description="Plano para testes automáticos",
            created_by=cls.auth_user_admin,
            updated_by=cls.auth_user_admin,
        )

        cls.vertical = Vertical.objects.create(
            name="Vertical Teste",
            created_by=cls.auth_user_admin,
            updated_by=cls.auth_user_admin,
        )

        cls.plan_id = cls.plan.id
        cls.vertical_id = cls.vertical.id
        
        

    @tag("unit")
    def test_plan_vertical_create_admin(self):
        payload = {
            "plan_id": self.plan.id,
            "vertical_id": self.vertical.id
        }

        response = self.client.post(
            path=self.plan_vertical_create_url,
            data=payload,
            format="json",
            **self.auth_headers_user_admin,
        )

        self.assertEqual(201, response.status_code)
        self.assertEqual(response.data["plan"]["id"], payload["plan_id"])
        self.assertEqual(response.data["vertical"]["id"], payload["vertical_id"])

    @tag("unit")
    def test_plan_vertical_create_editor(self):
        payload = {
            "plan_id": self.plan.id,
            "vertical_id": self.vertical.id
        }

        response = self.client.post(
            path=self.plan_vertical_create_url,
            data=payload,
            format="json",
            **self.auth_headers_editor,
        )

        self.assertEqual(201, response.status_code) 

    @tag("unit")
    def test_plan_vertical_create_reader(self):
        payload = {
            "plan_id": self.plan.id,
            "vertical_id": self.vertical.id
        }

        response = self.client.post(
            path=self.plan_vertical_create_url,
            data=payload,
            format="json",
            **self.auth_headers_reader,
        )

        self.assertEqual(201, response.status_code) 
    @tag("unit")
    def test_plan_vertical_create_invalid_ids(self):
        payload = {
            "plan_id": 9999, 
            "vertical_id": 9999
        }

        response = self.client.post(
            path=self.plan_vertical_create_url,
            data=payload,
            format="json",
            **self.auth_headers_user_admin,
        )

        self.assertEqual(404, response.status_code)
        self.assertEqual(response.data["detail"], "Invalid plan_id or vertical_id.")
