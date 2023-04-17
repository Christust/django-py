from django.urls import path
from apps.products.api.views.general_views import (
    MeasureUnitListAPIView,
    CategoryProductListAPIView,
    IndicatorListAPIView,
)
from apps.products.api.views.product_views import (
    # Se sustituyen por ListCreateAPIView
    # ProductListAPIView,
    # ProductCreateAPIView,
    ProductListCreateAPIView,
    # ProductRetrieveAPIView,
    # ProductDestroyAPIView,
    # ProductUpdateAPIView,
    ProductRetrieveUpdateDestroyAPIView,
)

urlpatterns = [
    path("measure_units", MeasureUnitListAPIView.as_view(), name="list_measure_units"),
    path("categories", CategoryProductListAPIView.as_view(), name="list_categories"),
    path("indicators", IndicatorListAPIView.as_view(), name="list_indicators"),
    #! Se sustituyen estas dos rutas por ListCreateAPIView
    # path("list_product", ProductListAPIView.as_view(), name="list_product"),
    # path("create_product", ProductCreateAPIView.as_view(), name="create_product"),
    path(
        "list_create_product",
        ProductListCreateAPIView.as_view(),
        name="list_create_product",
    ),
    #! Se sustituyen por RetrieveUpdateDestroyAPIView
    # path(
    #     "retrieve_product/<int:pk>",
    #     ProductRetrieveAPIView.as_view(),
    #     name="retrieve_product",
    # ),
    # path(
    #     "destroy_product/<int:pk>",
    #     ProductDestroyAPIView.as_view(),
    #     name="destroy_product",
    # ),
    # path(
    #     "update_product/<int:pk>", ProductUpdateAPIView.as_view(), name="update_product"
    # ),
    path(
        "retrieve_update_destroy_product/<int:pk>",
        ProductRetrieveUpdateDestroyAPIView.as_view(),
        name="retrieve_update_destroy",
    ),
]
