from django.db import models


# Create your models here.
class BaseModel(models.Model):
    id = models.AutoField(primary_key=True)
    state = models.BooleanField("Estado", default=True)
    created = models.DateField("Fecha de creación", auto_now=False, auto_now_add=True)
    updated = models.DateField(
        "Fecha de actualización", auto_now=True, auto_now_add=False
    )
    deleted = models.DateField(
        "Fecha de eliminación",
        auto_now=True,
        auto_now_add=False,
        null=True
    )

    class Meta:
        abstract = True
        verbose_name = "Modelo base"
        verbose_name_plural = "Modelos base"
