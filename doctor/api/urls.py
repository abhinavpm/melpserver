"""
URL configuration for Doctor API Endpoints.
"""
from django.urls import path

from doctor.api.views import (DoctorDetailView, DoctorListView,
                              DoctorProfileView, DoctorRegisterView)

app_name = "doctor-api"
urlpatterns = [
    path("list/", DoctorListView.as_view(), name="doctor-list"),
    path("register/", DoctorRegisterView.as_view(), name="doctor-register"),
    path("profile/", DoctorProfileView.as_view(), name="doctor-profile"),
    path("<int:pk>/", DoctorDetailView.as_view(), name="doctor-details"),
]
