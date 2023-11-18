from django.urls import path

from patient.api.views import (PatientDetailView, PatientListView,
                               PatientProfileView, PatientRegisterView)

app_name = "patient-api"
urlpatterns = [
    path("list", PatientListView.as_view(), name="user-list"),
    path("register", PatientRegisterView.as_view(), name="user-register"),
    path("<int:pk>", PatientDetailView.as_view(), name="user-details"),
    path("profile", PatientProfileView.as_view(), name="user-profile"),
]
