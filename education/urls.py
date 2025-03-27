from django.urls import path
from rest_framework.routers import DefaultRouter

from education.apps import EducationConfig

from .views import (CourseViewSet, LessonCreate, LessonDelete, LessonDetail,
                    LessonList, LessonUpdate)

app_name = EducationConfig.name

router = DefaultRouter()

router.register(r"courses", CourseViewSet, basename="course")

urlpatterns = [
    path("lessons/", LessonList.as_view(), name="lesson-list"),
    path("lessons/<int:pk>/", LessonDetail.as_view(), name="lesson-detail"),
    path("lessons/<int:pk>/update/", LessonUpdate.as_view(), name="lesson-update"),
    path("lessons/<int:pk>/delete/", LessonDelete.as_view(), name="lesson-delete"),
    path("lessons/create/", LessonCreate.as_view(), name="lesson-create"),
] + router.urls
