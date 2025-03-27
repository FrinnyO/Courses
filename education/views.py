from django.shortcuts import get_object_or_404, render
from rest_framework import generics, viewsets
from rest_framework.response import Response

from .models import Course, Lesson
from .serializers import CourseSerializer, LessonSerializer


class CourseViewSet(viewsets.ViewSet):

    def list(self, request):
        queryset = Course.objects.all()
        serializer = CourseSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Course.objects.all()
        course = get_object_or_404(queryset, pk=pk)
        serializer = CourseSerializer(course)
        return Response(serializer.data)

    def update(self, request, pk=None):
        queryset = Course.objects.all()
        course = get_object_or_404(queryset, pk=pk)
        serializer = CourseSerializer(course, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def partial_update(self, request, pk=None):
        queryset = Course.objects.all()
        course = get_object_or_404(queryset, pk=pk)
        serializer = CourseSerializer(course, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def create(self, request):
        serializer = CourseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        queryset = Course.objects.all()
        course = get_object_or_404(queryset, pk=pk)
        course.delete()
        return Response({"message": "Course deleted successfully"})


class LessonList(generics.ListCreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonCreate(generics.CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonDetail(generics.RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonUpdate(generics.UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonDelete(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
