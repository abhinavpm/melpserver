from django.http import Http404
from django.shortcuts import get_object_or_404, render
from drf_spectacular.utils import extend_schema
from rest_framework import authentication, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from account.api.serializers import UserSerializer
from doctor.api.permissions import IsDoctor
from doctor.api.serializers import DoctorRegisterSerializer, DoctorSerializer
from doctor.models import Doctor


# Create your views here.
@extend_schema(request=None, responses=DoctorRegisterSerializer)
class DoctorRegisterView(APIView):
    """
    Register a doctor to the system.
    """

    @extend_schema(responses=DoctorRegisterSerializer)
    def post(self, request):
        """
        Register the doctor.
        """
        serializer = DoctorRegisterSerializer(data=request.data)
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


@extend_schema(responses=DoctorSerializer)
class DoctorListView(APIView):
    """
    List the Doctors in the system.
    """

    # authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(responses=DoctorSerializer)
    def get(self, request, format=None):
        """
        Return a list of all users.
        """
        doctors = Doctor.objects.all()
        serializer = DoctorSerializer(doctors, many=True, context={"request": request})
        return Response(serializer.data)


@extend_schema(request=None, responses=DoctorSerializer)
class DoctorDetailView(APIView):
    """
    Retrieve, update or delete a Doctor instance.
    """

    # authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):
        try:
            return Doctor.objects.get(pk=pk)
        except Doctor.DoesNotExist:
            raise Http404

    @extend_schema(responses=DoctorSerializer)
    def get(self, request, pk, format=None):
        """
        Get the details of the doctor
        """
        doctor = self.get_object(pk)
        serializer = DoctorSerializer(doctor)
        return Response(serializer.data)

    @extend_schema(responses=DoctorSerializer)
    def put(self, request, pk, format=None):
        """
        Update the details of the doctor.
        """
        doctor = self.get_object(pk)
        serializer = DoctorSerializer(doctor, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(responses=DoctorSerializer)
    def delete(self, request, pk, format=None):
        """
        Remove the doctor from the system.
        """
        doctor = self.get_object(pk)
        doctor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(responses=DoctorSerializer)
class DoctorProfileView(APIView):
    """
    Retrieve details of logged in Doctor.
    """

    # authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(responses=DoctorSerializer)
    def get(self, request, format=None):
        """
        Get the details of the doctor
        """
        doctor = Doctor.objects.get(user=self.request.user)
        serializer = DoctorSerializer(doctor)
        return Response(serializer.data)
