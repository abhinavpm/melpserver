from django.contrib.auth import get_user_model
from rest_framework import serializers

from account.api.serializers import UserSerializer
from doctor.models import Doctor

UserModel = get_user_model()


class DoctorRegisterSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Doctor
        fields = (
            "user",
            "doctor_id",
            "experience",
            "education",
        )

    def create(self, validated_data):
        doctor_data = {
            "phone_number": validated_data.get("user").get("phone_number"),
            "full_name": validated_data.get("user").get("full_name"),
        }
        user_data = validated_data.get("user")
        user = UserModel.objects.create_user(**user_data, is_doctor=True)
        validated_data.update({"user": user})
        doctor = Doctor.objects.create(**validated_data, **doctor_data)
        return doctor


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = "__all__"
        extra_kwargs = {"doctor_id": {"read_only": True}}

    def update(self, instance, validated_data):
        user = instance.user
        user.full_name = validated_data.get("full_name", user.full_name)
        user.phone_number = validated_data.get("phone_number", user.phone_number)
        user.save()
        super().update(instance, validated_data)
        return instance
