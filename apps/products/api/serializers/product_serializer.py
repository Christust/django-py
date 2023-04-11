from apps.products.models import Product
from apps.products.api.serializers.general_serializer import (
    MeasureUnitSerializer,
    CategoryProductSerializer,
)
from rest_framework import serializers


class ProductSerializer(serializers.ModelSerializer):
    # measure_unit = serializers.StringRelatedField()
    # category = serializers.StringRelatedField()

    class Meta:
        model = Product
        exclude = ["state", "created", "updated", "deleted"]

    def to_representation(self, instance):
        return {
            "id": instance.id,
            "measure_unit": instance.measure_unit.description,
            "category": instance.category.description,
            "name": instance.name,
            "description": instance.description,
            "image": instance.image if instance.image != "" else "",
        }
