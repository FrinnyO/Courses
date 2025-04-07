from django.urls import reverse
from rest_framework import serializers, status
from rest_framework.test import APITestCase

from education.models import Course, Lesson
from users.models import User

from .models import Subscription


class SubscriptionTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="test_user@.com")
        self.course = Course.objects.create(
            title="Python", description="Python course", owner=self.user
        )

    def test_subscription(self):
        url = reverse("users:subscription")
        data = {"course": self.course.pk, "user": self.user.pk}
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Subscription.objects.all().count(), 1)
        self.assertEqual(Subscription.objects.get(id=1).course, self.course)
        self.assertEqual(Subscription.objects.get(id=1).user, self.user)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Subscription.objects.all().count(), 0)
