from rest_framework import serializers
from .validators import validate_video_link
from users.models import Subscription
from users.serializers import SubscriptionSerializer

from .models import Course, Lesson


class LessonSerializer(serializers.ModelSerializer):
    video_link = serializers.URLField(validators=[validate_video_link])

    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField(read_only=True)
    lessons = LessonSerializer(many=True, read_only=True)
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    def get_lessons_count(self, obj):
        return obj.lessons.count()

    def get_is_subscribed(self, obj):
        request = self.context.get("request", None)
        if request is None:
            return False
        return Subscription.objects.filter(course=obj, user=request.user).exists()

    class Meta:
        model = Course
        fields = "__all__"
