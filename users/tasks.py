from celery import shared_task
from django.utils import timezone

from .models import User


@shared_task
def check_user_status():
    today = timezone.now()
    all_users = User.objects.all()
    for user in all_users:
        last_login = user.last_login
        if last_login is not None:
            time_difference = today - last_login
            if time_difference.days > 30:
                if not user.is_staff:
                    user.is_active = False
                    user.save()
        else:
            print(f"User {user.email} has never logged in.")
