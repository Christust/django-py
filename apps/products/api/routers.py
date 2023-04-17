from rest_framework import routers
from apps.products.api.views.product_views import ProductViewSet

router = routers.DefaultRouter()

router.register(r"product", ProductViewSet)

urlpatterns = router.urls