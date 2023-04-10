from django.urls import path
from apps.products.api.views.general_views import (
    MeasureUnitListAPIView,
    CategoryProductListAPIView,
    IndicatorListAPIView,
)

urlpatterns = [
    path("measure_units", MeasureUnitListAPIView.as_view(), name="list_measure_units"),
    path("categories", CategoryProductListAPIView.as_view(), name="list_categories"),
    path("indicators", IndicatorListAPIView.as_view(), name="list_indicators"),
]
