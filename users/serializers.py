from rest_framework import serializers

from .models import Payment, User


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            "id",
            "user",
            "payment_date",
            "paid_course",
            "paid_lesson",
            "amount",
            "payment_method",
        ]


class UserSerializer(serializers.ModelSerializer):
    payments = PaymentSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ["id", "email", "phone_number", "city", "payments"]
