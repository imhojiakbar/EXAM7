from django.contrib import admin

from apps.main.models import Category, Product, ProductLike


@admin.register(ProductLike)
class ProductLikeAdmin(admin.ModelAdmin):
    pass