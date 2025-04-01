from django.core.management.base import BaseCommand

from education.models import Course, Lesson


class Command(BaseCommand):
    def handle(self, *args, **options):
        python, created = Course.objects.get_or_create(
            title="Python", defaults={"description": "Python course"}
        )
        django, created = Course.objects.get_or_create(
            title="Django", defaults={"description": "Django course"}
        )
        flask, created = Course.objects.get_or_create(
            title="Flask", defaults={"description": "Flask course"}
        )

        Lesson.objects.get_or_create(
            title="Lesson 1",
            defaults={"description": "Description 1", "course": python},
        )
        Lesson.objects.get_or_create(
            title="Lesson 2",
            defaults={"description": "Description 2", "course": django},
        )
        Lesson.objects.get_or_create(
            title="Lesson 3", defaults={"description": "Description 3", "course": flask}
        )

        self.stdout.write(
            self.style.SUCCESS("Successfully created or retrieved courses and lessons")
        )
