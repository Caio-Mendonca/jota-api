from django.urls import path


from .apis.plan_create_api import plan_create_api
from .apis.plan_edit_api import plan_edit_api
app_name = "plan"

urlpatterns = [
    path("create/", plan_create_api, name="create"),
    path("edit/<int:pk>/", plan_edit_api, name="edit"),
]