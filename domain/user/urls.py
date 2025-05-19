from django.urls import path
from .apis.user_activate_api import user_activate_and_create_password_api

# from .apis.user_reset_password_api import user_reset_password_api
# from .apis.user_altered_password_api import user_altered_password_api
# from .apis.user_send_email_reset_password_api import user_send_email_reset_password_api
from .apis.user_create_api import user_create_api

# from .apis.user_delete_api import user_delete_api
from .apis.user_detail_api import user_detail_api
from .apis.user_list_api import user_list_api
from .apis.user_update_api import user_update_api

urlpatterns = [
    path("", user_list_api, name="list"),
    path("<int:pk>/", user_detail_api, name="detail"),
    path("create/", user_create_api, name="create"),
    path("<int:pk>/update/", user_update_api, name="update"),
    # path(
    #     "<int:pk>/update_password/", user_altered_password_api, name="update_password"
    # ),
    path("activate/<uid>/", user_activate_and_create_password_api, name="activate"),
    # path("<int:pk>/delete/", user_delete_api, name="delete"),
    # path(
    #     "send_email_reset_password/",
    #     user_send_email_reset_password_api,
    #     name="send_email_reset_password",
    # ),
    # path("reset_password/<uid>/", user_reset_password_api, name="reset_password"),
]
