from django.contrib.auth import get_user_model
from django.http import Http404
from django.shortcuts import get_object_or_404, render
from drf_spectacular.utils import extend_schema
from rest_framework import authentication, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from patient.api.permissions import IsUserOrDoctor
from patient.api.serializers import (PatientRegisterSerializer,
                                     PatientSerializer)
from patient.models import Patient

UserModel = get_user_model()


@extend_schema(responses=PatientSerializer)
class PatientListView(APIView):
    """
    List the User in the system.
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        patients = Patient.objects.all()
        serializers = PatientSerializer(patients, many=True)
        data = serializers.data
        return Response(data)


@extend_schema(request=PatientRegisterSerializer, responses=PatientRegisterSerializer)
class PatientRegisterView(APIView):
    """
    Registers the Users to the system.
    """

    @extend_schema(request=PatientRegisterSerializer)
    def post(self, request):
        """
        Register the patient.
        """
        serializer = PatientRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )


@extend_schema(request=PatientSerializer, responses=PatientSerializer)
class PatientDetailView(APIView):

    """
    Retrieve, update or delete a User instance.
    """

    permission_classes = [IsUserOrDoctor, permissions.IsAuthenticated]

    @extend_schema(responses=PatientSerializer)
    def get_object(self, request, pk):
        try:
            return Patient.objects.get(pk=pk)
        except Patient.DoesNotExist:
            return Response(
                {"error": "Patient not found"}, status=status.HTTP_404_NOT_FOUND
            )

    @extend_schema(request=PatientSerializer)
    def get(self, request, pk):
        """
        Retreive the User in the system
        """
        patient = self.get_object(request, pk)
        serializer = PatientSerializer(patient)
        return Response(serializer.data)

    @extend_schema(request=PatientSerializer)
    def delete(self, request, pk):
        """
        Remove the User from the system.
        """
        patient = self.get_object(request, pk)
        patient.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @extend_schema(request=PatientSerializer)
    def put(self, request, pk):
        """
        Update the user in the system
        """
        patient = self.get_object(request, pk)
        serializer = PatientSerializer(
            instance=patient, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_200_OK,
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PatientProfileView(APIView):
    """
    Retrieve details of logged in User.
    """

    permission_classes = [IsUserOrDoctor, permissions.IsAuthenticated]

    @extend_schema(responses=PatientSerializer)
    def get(self, request):
        try:
            patient = Patient.objects.get(user=self.request.user)
            serializer = PatientSerializer(patient)
            return Response(serializer.data)
        except Patient.DoesNotExist:
            return Response("Patient not found", status=status.HTTP_404_NOT_FOUND)
