from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, views
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from education.models import Course

from .models import Payment, Subscription, User
from .permissions import IsAdmin, IsOwner
from .serializers import (OtherUserSerializer, PaymentSerializer,
                          SubscriptionSerializer, UserSerializer,
                          UserTokenObtainPairSerializer)


class UserListAPIView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = OtherUserSerializer


class UserCreateAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            self.permission_classes = [AllowAny]
        return super().get_permissions()

    def perform_create(self, serializer):
        user = serializer.save()
        user.set_password(user.password)
        user.is_active = True
        user.save()


class UserUpdateAPIView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsOwner,)


class UserDestroyAPIView(generics.DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)


class UserRetrieveAPIView(generics.RetrieveAPIView):
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.get_object() == self.request.user:
            return UserSerializer
        return OtherUserSerializer


class PaymentListAPIView(generics.ListCreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["payment_method", "paid_course", "paid_lesson"]
    ordering_fields = ["payment_date"]


class UserTokenObtainPairView(TokenObtainPairView):
    serializer_class = UserTokenObtainPairSerializer
    permission_classes = [AllowAny]


class SubscriptionAPIView(views.APIView):

    serializer_class = SubscriptionSerializer

    def post(self, *args, **kwargs):
        user = self.request.user
        course_id = self.request.data.get("course")
        course_item = get_object_or_404(Course, pk=course_id)

        subs_item = Subscription.objects.filter(user=user, course=course_item)

        if subs_item.exists():
            subs_item.delete()
            message = "Deleted subscription"
        else:
            Subscription.objects.create(user=user, course=course_item)
            message = "Added subscription"
        return Response({"message": message})
