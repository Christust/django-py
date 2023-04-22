from apps.users.api import api
from rest_framework import routers

router = routers.DefaultRouter()

router.register(r"", api.UserAPIView)

urlpatterns = router.urls
