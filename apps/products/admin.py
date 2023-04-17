from django.contrib import admin
from .models import *


# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name")


admin.site.register(Product, ProductAdmin)
admin.site.register(Indicator)
admin.site.register(CategoryProduct)
admin.site.register(MeasureUnit)
