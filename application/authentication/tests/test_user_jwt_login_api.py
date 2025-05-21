import os.path

from domain.user.actions import user_create

PROJECT_ROOT = os.path.dirname(os.path.realpath(__name__))

from django.urls import reverse
from django.conf import settings
from django.contrib.auth.models import Group
from django.test import TestCase, tag
from unittest.mock import patch
from rest_framework.test import APIClient


class UserJwtLoginTests(TestCase):
    fixtures = [PROJECT_ROOT + "/fixtures/db_test.json"]

    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()

        cls.jwt_login_url = reverse("api:auth:login")
        cls.me_url = reverse("api:auth:me")

        cls.user_admin = {
            "name": "Test 1",
            "email": "adm@example.com",
            "password": "senhaADM",
            "is_active": True,
            "group": Group.objects.get(id=1),
        }

        user_create(**cls.user_admin)

    @tag("unit")
    def test_user_login_invalid_credentials(self):
        data = {"email": "adm@example.com", "password": "test122345"}

        response = self.client.post(path=self.jwt_login_url, data=data)

        self.assertEqual(401, response.status_code)

    @tag("unit")
    def test_user_login_valid_credentials(self):
        data = {"email": "adm@example.com", "password": "senhaADM"}

        response = self.client.post(path=self.jwt_login_url, data=data)

        self.assertEqual(200, response.status_code)