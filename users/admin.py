from django.contrib import admin

from .models import User


@admin.register(User)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "email",
    )
    search_fields = ("email",)
