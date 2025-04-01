from django.shortcuts import get_object_or_404, render
from rest_framework import generics, status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Course, Lesson
from .permissions import IsModerator, IsOwner
from .serializers import CourseSerializer, LessonSerializer


class CourseViewSet(viewsets.ViewSet):

    def list(self, request):
        if request.user.groups.filter(name="Moderator").exists():
            queryset = Course.objects.all()
        else:
            queryset = Course.objects.filter(owner=request.user)
        serializer = CourseSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        course = get_object_or_404(Course, pk=pk)
        if not (
            IsOwner().has_object_permission(request, self, course)
            or IsModerator().has_permission(request, self)
        ):
            return Response(
                {"detail": "You do not have permission to perform this action."},
                status=status.HTTP_403_FORBIDDEN,
            )
        serializer = CourseSerializer(course)
        return Response(serializer.data)

    def partial_update(self, request, pk=None):
        course = get_object_or_404(Course, pk=pk)
        if not (
            IsOwner().has_object_permission(request, self, course)
            or IsModerator().has_permission(request, self)
        ):
            return Response(
                {"detail": "You do not have permission to perform this action."},
                status=status.HTTP_403_FORBIDDEN,
            )
        serializer = CourseSerializer(course, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def create(self, request):
        serializer = CourseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(owner=request.user)
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        course = get_object_or_404(Course, pk=pk)
        if not IsOwner().has_object_permission(request, self, course):
            return Response(
                {"detail": "You do not have permission to perform this action."},
                status=status.HTTP_403_FORBIDDEN,
            )
        course.delete()
        return Response(
            {"message": "Course deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = (~IsModerator, IsAuthenticated)
        elif self.action == "destroy":
            self.permission_classes = (IsOwner,)
        elif self.action in ["update", "partial_update", "retrieve"]:
            self.permission_classes = (IsOwner | IsModerator,)
        return super().get_permissions()


class LessonList(generics.ListCreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = (~IsModerator & IsOwner | IsModerator,)

    def get_queryset(self):
        if self.request.user.groups.filter(name="Moderator").exists():
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=self.request.user)


class LessonCreate(generics.CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [~IsModerator & IsAuthenticated]

    def perform_create(self, serializer):
        lesson = serializer.save()
        lesson.owner = self.request.user
        lesson.save()


class LessonDetail(generics.RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsOwner | IsModerator,)


class LessonUpdate(generics.UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsOwner | IsModerator,)


class LessonDelete(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsOwner,)
