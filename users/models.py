from django.contrib.auth.models import AbstractUser
from django.db import models

from education.models import Course, Lesson


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    phone_number = models.CharField(
        max_length=15, blank=True, null=True, verbose_name="Phone_number"
    )
    city = models.CharField(max_length=50, blank=True, null=True, verbose_name="City")
    avatar = models.ImageField(
        upload_to="avatars/",
        default="users/default_avatar.jpg",
        blank=True,
        null=True,
        verbose_name="Avatar",
    )

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = [
            "email",
        ]

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


class Payment(models.Model):

    PAYMENT_METHOD_CHOICES = [
        ("Cash", "Cash"),
        ("Transfer", "Transfer"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="payments",
        verbose_name="Payment",
    )
    payment_date = models.DateTimeField(auto_now_add=True, verbose_name="Payment date")
    paid_course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="payments",
        verbose_name="Paid course",
    )
    paid_lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="payments",
        verbose_name="Paid lesson",
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Amount")
    payment_method = models.CharField(
        max_length=20, choices=PAYMENT_METHOD_CHOICES, verbose_name="Payment method"
    )
    session_id = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="Session ID"
    )
    link = models.URLField(max_length=400, blank=True, null=True, verbose_name="Link")

    class Meta:
        verbose_name = "Payment"
        verbose_name_plural = "Payments"
        ordering = ["-payment_date"]

    def __str__(self):
        return f"{self.user} - {self.payment_date}"


class Subscription(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="subscriptions",
        verbose_name="User",
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="subscriptions",
        verbose_name="Course",
    )

    class Meta:
        verbose_name = "Subscription"
        verbose_name_plural = "Subscriptions"
        unique_together = ["user", "course"]

    def __str__(self):
        return f"{self.user} - {self.course}"
