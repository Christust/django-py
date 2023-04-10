from apps.products.api.serializers import general_serializer
from apps.base.api import GeneralListAPIView


class MeasureUnitListAPIView(GeneralListAPIView):
    serializer_class = general_serializer.MeasureUnitSerializer


class IndicatorListAPIView(GeneralListAPIView):
    serializer_class = general_serializer.IndicatorSerializer


class CategoryProductListAPIView(GeneralListAPIView):
    serializer_class = general_serializer.CategoryProductSerializer
