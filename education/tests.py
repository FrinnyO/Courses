from django.contrib.auth.models import Group
from django.urls import reverse
from rest_framework import serializers, status
from rest_framework.test import APITestCase, force_authenticate

from users.models import User

from .models import Course, Lesson


class CourseTestCase(APITestCase):
    def setUp(self):
        moderators_group, created = Group.objects.get_or_create(name="Moderator")
        self.user = User.objects.create(email="test_user@.com")
        self.moderator = User.objects.create(email="moderator@.com", is_staff=True)
        moderators_group.user_set.add(self.moderator)
        self.course = Course.objects.create(
            title="Python", description="Python course", owner=self.user
        )
        self.lesson = Lesson.objects.create(
            title="Lesson 1", description="Description 1", course=self.course
        )

    def test_create_course(self):
        url = reverse("education:course-list")
        data = {"title": "Django", "description": "Django course"}
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Course.objects.all().count(), 2)
        self.client.force_authenticate(user=self.moderator)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_courses(self):
        url = reverse("education:course-list")
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Course.objects.all().count(), 1)
        self.client.force_authenticate(user=self.moderator)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Course.objects.all().count(), 1)

    def test_course_retrieve(self):
        url = reverse("education:course-detail", args=[self.course.pk])
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Python")
        self.client.force_authenticate(user=self.moderator)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_course_update(self):
        url = reverse("education:course-detail", args=[self.course.pk])
        data = {"title": "Django", "description": "Django course"}
        self.client.force_authenticate(user=self.user)
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Course.objects.get(id=self.course.pk).title, "Django")
        self.client.force_authenticate(user=self.moderator)
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_course_partial_update(self):
        url = reverse("education:course-detail", args=[self.course.pk])
        data = {"title": "Django"}
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Course.objects.get(id=self.course.pk).title, "Django")
        self.client.force_authenticate(user=self.moderator)
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_course_delete(self):
        url = reverse("education:course-detail", args=[self.course.pk])
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Course.objects.all().count(), 0)
        self.client.force_authenticate(user=self.moderator)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class LessonTestCase(APITestCase):

    def setUp(self):
        moderators_group, created = Group.objects.get_or_create(name="Moderator")
        self.user = User.objects.create(email="test_user@.com")
        self.moderator = User.objects.create(email="moderator@.com", is_staff=True)
        moderators_group.user_set.add(self.moderator)
        self.course = Course.objects.create(
            title="Python", description="Python course", owner=self.user
        )
        self.lesson = Lesson.objects.create(
            title="Lesson 1",
            description="Description 1",
            course=self.course,
            owner=self.user,
        )

    def test_create_lesson(self):
        url = reverse("education:lesson-create")
        data = {
            "title": "Lesson 2",
            "description": "Description 2",
            "course": self.course.pk,
            "video_link": "https://www.youtube.com/watch?v=wCirsvWAsiE",
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.get(title="Lesson 2").owner, self.user)
        self.assertEqual(Lesson.objects.all().count(), 2)
        self.client.force_authenticate(user=self.moderator)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        data = {
            "title": "Lesson 2",
            "description": "Description 2",
            "course": self.course.pk,
            "video_link": "https://www.video.com/watch?v=wCirsvWAsiE",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertRaises(serializers.ValidationError)

    def test_retrieve_lesson(self):
        url = reverse("education:lesson-detail", args=[self.lesson.pk])
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Lesson 1")
        self.client.force_authenticate(user=self.moderator)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_lesson(self):
        url = reverse("education:lesson-update", args=[self.lesson.pk])
        data = {
            "title": "Lesson 2",
            "description": "Description 2",
            "course": self.course.pk,
            "video_link": "https://www.youtube.com/watch?v=wCirsvWAsiE",
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Lesson.objects.get(id=self.lesson.pk).title, "Lesson 2")

    def test_lessons_list(self):
        url = reverse("education:lesson-list")
        course = Course.objects.create(title="Django", description="Django course")
        Lesson.objects.create(
            title="Lesson 3", description="Description 3", course=course
        )
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(Lesson.objects.all().count(), 2)

    def test_delete_lesson(self):
        url = reverse("education:lesson-delete", args=[self.lesson.pk])
        self.client.force_authenticate(user=self.moderator)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
