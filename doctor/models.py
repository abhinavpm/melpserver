import os
import uuid
from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from multiselectfield import MultiSelectField

from account.validators import PhoneNumberValidator

UserModel = get_user_model()


def custom_file_name(instance, filename):
    # Get the file extension
    extension = os.path.splitext(filename)[1]
    unique_id = uuid.uuid4().hex

    new_filename = f"{instance.id}_{unique_id}{extension}"
    return new_filename


def upload_profile_photo(instance, filename):
    return f"media/profile/doctor/{custom_file_name(instance, filename)}"


# Create your models here.
class Doctor(models.Model):
    phone_validator = PhoneNumberValidator()

    class ServiceMode(models.TextChoices):
        MODE1 = "both", _("Both")
        MODE2 = "clinic", _("Clinic")
        MODE3 = "visiting", _("Visiting")

    class Gender(models.TextChoices):
        MALE = "male", _("Male")
        FEMALE = "female", _("Female")
        OTHER = "other", _("Other")

    phone_number = models.CharField(
        _("phone number"),
        max_length=13,
        unique=True,
        help_text=_("Required. 10 digits only."),
        validators=[phone_validator],
        error_messages={
            "unique": _("A user with that phone number already exists."),
        },
    )
    full_name = models.CharField(_("full name"), max_length=150)
    user = models.OneToOneField(
        UserModel, on_delete=models.CASCADE, related_name="doctor_profile"
    )
    age = models.IntegerField(_("age"), null=True, blank=True)
    gender = models.CharField(_("gender"), choices=Gender.choices, max_length=10)
    bio = models.TextField(_("bio"), blank=True, null=True)
    experience = models.IntegerField(_("experience"), null=True, blank=True)
    education = models.CharField(_("education"), max_length=100, null=True, blank=True)
    hospital = models.CharField(_("hospital"), max_length=100, null=True, blank=True)
    mode_of_service = MultiSelectField(
        _("service mode"), max_length=10, choices=ServiceMode.choices, max_choices=1
    )
    time_slot_days = models.JSONField(_("time slot day"), null=True, blank=True)
    time_slot_times = models.JSONField(_("time slot time"), null=True, blank=True)
    status_of_availability = models.BooleanField(
        _("status of availability"),
        default=False,
    )
    doctor_id = models.CharField(_("doctors ID"), max_length=15, unique=True)
    consultation_fee = models.IntegerField(_("consultation fee"), default=0.0)
    profile_picture = models.ImageField(
        _("profile_picture"), upload_to=upload_profile_photo, null=True, blank=True
    )

    def __str__(self) -> str:
        return f"{self.user.full_name} ({self.user.phone_number})"
