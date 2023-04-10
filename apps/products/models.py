from django.db import models
from simple_history.models import HistoricalRecords
from apps.base.models import BaseModel


# Create your models here.
class MeasureUnit(BaseModel):
    """Model definition for MeasureUnit."""

    # TODO: Define fields here
    description = models.CharField(
        "Descripción", max_length=50, blank=False, null=False, unique=True
    )
    historical = HistoricalRecords()

    @property
    def _history_user(self):
        return self.change_by

    @_history_user.setter
    def _history_user(self, value):
        self.change_by = value

    class Meta:
        """Meta definition for MeasureUnit."""

        verbose_name = "Unidad de medida"
        verbose_name_plural = "Unidades de medida"

    def __str__(self):
        return self.description


class CategoryProduct(BaseModel):
    """Model definition for CategoryProduct."""

    # TODO: Define fields here
    description = models.CharField(max_length=50, blank=False, null=False, unique=True)
    historical = HistoricalRecords()

    @property
    def _history_user(self):
        return self.change_by

    @_history_user.setter
    def _history_user(self, value):
        self.change_by = value

    class Meta:
        """Meta definition for CategoryProduct."""

        verbose_name = "Categoria de producto"
        verbose_name_plural = "Categorias de producto"

    def __str__(self):
        return self.description


class Indicator(BaseModel):
    """Model definition for Indicator."""

    # TODO: Define fields here
    descount_value = models.PositiveSmallIntegerField(default=0)
    category_product = models.ForeignKey(
        CategoryProduct, on_delete=models.CASCADE, verbose_name="Indicador de oferta"
    )
    historical = HistoricalRecords()

    @property
    def _history_user(self):
        return self.change_by

    @_history_user.setter
    def _history_user(self, value):
        self.change_by = value

    class Meta:
        """Meta definition for Indicator."""

        verbose_name = "Indicador de oferta"
        verbose_name_plural = "Indicadores de oferta"

    def __str__(self):
        return f"Oferta de la categoria {self.category_product}: {self.descount_value}%"


class Product(BaseModel):
    """Model definition for Product."""

    # TODO: Define fields here
    name = models.CharField(max_length=150, blank=False, null=False, unique=True)
    description = models.TextField("Descripción del producto", blank=False, null=False)
    image = models.ImageField(
        "Imagen del producto", upload_to="product/", blank=True, null=True
    )
    measure_unit = models.ForeignKey(
        MeasureUnit,
        on_delete=models.CASCADE,
        verbose_name="Unidad de medida",
        default=None,
    )
    category = models.ForeignKey(
        CategoryProduct, on_delete=models.CASCADE, verbose_name="Categoria"
    )
    historical = HistoricalRecords()

    @property
    def _history_user(self):
        return self.change_by

    @_history_user.setter
    def _history_user(self, value):
        self.change_by = value

    class Meta:
        """Meta definition for Product."""

        verbose_name = "Producto"
        verbose_name_plural = "Productos"

    def __str__(self):
        return self.name
