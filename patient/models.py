import uuid

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from doctor.models import Doctor

UserModel = get_user_model()


def custom_file_name(instance, filename):
    # Get the file extension
    extension = os.path.splitext(filename)[1]
    unique_id = uuid.uuid4().hex

    new_filename = f"{instance.id}_{unique_id}{extension}"
    return new_filename


def upload_profile_photo(instance, filename):
    return f"media/profile/doctor/{custom_file_name(instance, filename)}"

def upload_medical_history(instance, filename):
    return f"media/medicalhistory/{custom_file_name(instance, filename)}"


class Patient(models.Model):
    class Gender(models.TextChoices):
        MALE = "male", _("Male")
        FEMALE = "female", _("Female")
        OTHER = "other", _("Other")

    user = models.OneToOneField(UserModel, on_delete=models.CASCADE)
    phone_number = models.IntegerField(_("phone_number"), unique=True)
    full_name = models.CharField(_("fullname"), max_length=50)
    age = models.IntegerField(_("age"), null=True, blank=True)
    gender = models.CharField(_("Gender"), max_length=10, choices=Gender.choices)
    emergency_contact = models.IntegerField(
        _("Emergency_contact"), null=True, blank=True
    )
    blood_group = models.CharField(
        _("blood_group"), max_length=10, null=True, blank=True
    )
    profile_picture = models.ImageField(
        _("profile_picture"), upload_to=upload_profile_photo, null=True, blank=True
    )
    height = models.IntegerField(_("height"), null=True, blank=True)
    weight = models.IntegerField(_("weight"), null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.user.full_name} ({self.user.phone_number})"


class Consultation(models.Model):
    patient = models.OneToOneField(Patient, on_delete=models.CASCADE)
    consultaion_date = models.DateField()
    consultaion_time = models.TimeField()
    doctor_report = models.CharField(max_length=300)
    doctor = models.OneToOneField(Doctor, on_delete=models.CASCADE)


class MedicalHistory(models.Model):
    file = models.FileField( _("medical history file"), upload_to=upload_medical_history, null=True, blank=True)
    type = models.CharField( _("file type"), max_length=20, null=True, blank=True)
    patient = models.OneToOneField(Patient, on_delete=models.CASCADE)
