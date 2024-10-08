from django.contrib import admin
from shop import models


@admin.register(models.Picture)
class PictureAdmin(admin.ModelAdmin):
    list_display = ("title", "author")


@admin.register(models.Painter)
class PainterAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name")


@admin.register(models.Biography)
class BiographyAdmin(admin.ModelAdmin):
    list_display = ("biography_text", "contact_info")


@admin.register(models.Style)
class StyleAdmin(admin.ModelAdmin):
    list_display = ("style_name",)


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("category_name",)
