from apps.users.api import api
from django.urls import path

urlpatterns = [
    path("", api.UserAPIView.as_view(), name="usuario_api"),
    path("get_users", api.user_api_view, name="get_users_function"),
    path("get_user/<int:pk>", api.user_detail_view, name="get_user_detail"),
]
