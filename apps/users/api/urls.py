from apps.users.api import api
from django.urls import path

urlpatterns = [
    path("", api.UserAPIView.as_view(), name="usuario_api"),
    path("get_user", api.user_api_view, name="get_user_function"),
]
