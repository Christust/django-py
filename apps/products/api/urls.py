from django.urls import path
from apps.products.api.views.general_views import (
    MeasureUnitListAPIView,
    CategoryProductListAPIView,
    IndicatorListAPIView,
)
from apps.products.api.views.product_views import (
    ProductListAPIView,
    ProductCreateAPIView,
)

urlpatterns = [
    path("measure_units", MeasureUnitListAPIView.as_view(), name="list_measure_units"),
    path("categories", CategoryProductListAPIView.as_view(), name="list_categories"),
    path("indicators", IndicatorListAPIView.as_view(), name="list_indicators"),
    path("product", ProductListAPIView.as_view(), name="list_product"),
    path("create_product", ProductCreateAPIView.as_view(), name="create_product"),
]
