import random
from time import sleep

from django.core.management.base import BaseCommand

from education.models import Course, Lesson
from users.models import Payment, User


class Command(BaseCommand):

    def handle(self, *args, **options):
        test_users = User.objects.filter(email__startswith="user_")
        Payment.objects.filter(user__email__startswith="user_").delete()
        python_course = Course.objects.get(title="Python")
        django_course = Course.objects.get(title="Django")
        flask_course = Course.objects.get(title="Flask")
        courses_list = [python_course, django_course, flask_course]

        python_lessons = Lesson.objects.filter(course=python_course)
        django_lessons = Lesson.objects.filter(course=django_course)
        flask_lessons = Lesson.objects.filter(course=flask_course)
        lessons_list = [python_lessons, django_lessons, flask_lessons]

        for user in test_users:
            Payment.objects.get_or_create(
                user=user,
                amount=random.randint(100, 200),
                payment_method="Cash",
                paid_lesson=random.choice(random.choice(lessons_list)),
            )
            Payment.objects.get_or_create(
                user=user,
                amount=random.randint(1000, 2000),
                payment_method="Transfer",
                paid_course=random.choice(courses_list),
            )
            sleep(0.3)
        self.stdout.write(
            self.style.SUCCESS("Successfully created payments for test users")
        )
