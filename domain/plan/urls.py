from django.urls import path


from .apis.plan_create_api import plan_create_api

app_name = "plan"

urlpatterns = [
    path("create/", plan_create_api, name="create"),
]