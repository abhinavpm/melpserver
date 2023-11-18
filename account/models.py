# Create your models here.
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .validators import PhoneNumberValidator


class PhoneUserManager(UserManager):
    use_in_migrations = True

    def _create_user(self, phone_number, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not phone_number:
            raise ValueError("The given phone_number must be set")
        email = self.normalize_email(email)
        user = self.model(phone_number=phone_number, email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone_number, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(phone_number, email, password, **extra_fields)

    def create_superuser(self, phone_number, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(phone_number, email, password, **extra_fields)


class AbstractUser(AbstractBaseUser, PermissionsMixin):
    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.

    Phone number and password are required. Other fields are optional.
    """

    phone_validator = PhoneNumberValidator()

    username = None
    phone_number = models.CharField(
        _("phone number"),
        max_length=10,
        unique=True,
        help_text=_("Required. 10 digits only."),
        validators=[phone_validator],
        error_messages={
            "unique": _("A user with that phone number already exists."),
        },
    )
    full_name = models.CharField(_("full name"), max_length=150)
    email = models.EmailField(_("email address"), blank=True)
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    is_admin = models.BooleanField(
        _("admin"),
        default=False,
        help_text=_("Designates whether this user should be treated as admin."),
    )
    is_doctor = models.BooleanField(
        _("doctor"),
        default=False,
        help_text=_("Designates whether this user should be treated as doctor."),
    )
    is_partner = models.BooleanField(
        _("partner"),
        default=False,
        help_text=_("Designates whether this user should be treated as partner."),
    )
    is_user = models.BooleanField(
        _("user"),
        default=False,
        help_text=_("Designates whether this user should be treated as user."),
    )

    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    otp = models.IntegerField(blank=True, null=True)
    verified = models.BooleanField(
        _("Verification"),
        default=False,
        help_text=_("Designates whether this user is verified."),
    )

    objects = PhoneUserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = ["full_name"]

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        abstract = True
        db_table = "auth_user"

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def __str__(self):
        return self.phone_number

    @staticmethod
    def has_perm(perm, obj=None, **kwargs):
        return True

    @staticmethod
    def has_module_perms(app_label, **kwargs):
        return True


class User(AbstractUser):
    pass
