from django.urls import path

from domain.vertical.apis.plan_vertical_create_api import plan_vertical_create_api
from domain.vertical.apis.create_vertical_api import vertical_create_api
app_name = "vertical"

urlpatterns = [
    path("create/", vertical_create_api, name="create"),
    path("create_relation_plan/", plan_vertical_create_api, name="create_relation"),
]