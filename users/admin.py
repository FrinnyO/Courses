from django.contrib import admin

from .models import Payment, Subscription, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "email",
    )
    search_fields = ("email",)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "payment_date",
        "paid_course",
        "paid_lesson",
        "amount",
        "payment_method",
    )
    search_fields = ("user",)


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "course",
    )
    search_fields = ("user",)
