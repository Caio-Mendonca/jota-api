import os.path

from domain.vertical.models import Vertical

PROJECT_ROOT = os.path.dirname(os.path.realpath(__name__))

from domain.news.actions import news_create
from domain.user.selectors import user_get
from support.utils import get_tokens_for_user
from django.test import tag
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from django.conf import settings


class NewsDetailApiTests(APITestCase):
    fixtures = [PROJECT_ROOT + "/fixtures/db_test.json"]

    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()

        cls.news_detail_url = lambda pk: reverse("api:news:detail", kwargs={"pk": pk})

        cls.auth_user_with_perm = user_get(user_id=1)
        tokens = get_tokens_for_user(cls.auth_user_with_perm)
        access_with_perm = tokens["access"]
        cls.auth_headers_with_perm = {
            "HTTP_AUTHORIZATION": f"{settings.SIMPLE_JWT['AUTH_HEADER_TYPES']} {access_with_perm}"
        }


    def setUp(self) -> None:
        self.vertical = Vertical.objects.create(name="Vertical para Testes")

        new_news = {
            "title": "Notícia para Teste",
            "subtitle": "Subtitulo para teste",
            "content": "Conteúdo para teste da notícia",
            "status": "draft",
            "access_pro": False,
            "author": self.auth_user_with_perm,
            "vertical": self.vertical,  
        }

        self.news = news_create(
            title=new_news["title"],
            subtitle=new_news["subtitle"],
            content=new_news["content"],
            status=new_news["status"],
            access_pro=new_news["access_pro"],
            author=new_news["author"],
            vertical=new_news["vertical"],
        )

    @tag("unit")
    def test_news_detail_success(self):
        pk = self.news.pk
        response = self.client.get(
            path=self.news_detail_url(pk),
            format="json",
            **self.auth_headers_with_perm,
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("title", response.data)

    @tag("unit")
    def test_news_detail_not_found(self):
        pk = 999999 
        response = self.client.get(
            path=self.news_detail_url(pk),
            format="json",
            **self.auth_headers_with_perm,
        )
        self.assertEqual(response.status_code, 404)
