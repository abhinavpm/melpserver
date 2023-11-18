from django.contrib.auth import get_user_model
from rest_framework import serializers

from account.api.serializers import UserSerializer
from doctor.models import Doctor
from patient.models import Patient

UserModel = get_user_model()


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = "__all__"


class PatientRegisterSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Patient
        fields = ("user", "age", "emergency_contact", "gender", "blood_group")

    def create(self, validated_data):
        patient_data = {
            "phone_number": validated_data.get("user").get("phone_number"),
            "full_name": validated_data.get("user").get("full_name"),
        }
        user_data = validated_data.get("user")
        user = UserModel.objects.create_user(**user_data, is_user=True)
        validated_data.update({"user": user})
        patient = Patient.objects.create(**validated_data, **patient_data)
        return patient


class DocSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ("full_name", "experience", "education", "doctor_id")
