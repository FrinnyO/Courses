from celery import shared_task
from django.core.mail import send_mail

from config import settings
from users.models import Subscription


@shared_task
def send_update_course_message(course):
    subscriptions = Subscription.objects.filter(course=course["id"])
    for subscription in subscriptions:
        send_mail(
            f"Course {course["title"]} updated",
            f"Dear {subscription.user.email}, course {course["title"]} was updated",
            settings.DEFAULT_FROM_EMAIL,
            [subscription.user.email],
        )
