from django.urls import path
from .apis.user_activate_api import user_activate_and_create_password_api
from .apis.user_create_api import user_create_api
from .apis.user_detail_api import user_detail_api
from .apis.user_list_api import user_list_api
from .apis.user_update_api import user_update_api

urlpatterns = [
    path("create/", user_create_api, name="create"),
    path("activate/<uid>/", user_activate_and_create_password_api, name="activate"),
    path("<int:pk>/update/", user_update_api, name="update"),
    path("<int:pk>/", user_detail_api, name="detail"),
    path("", user_list_api, name="list"),
]
