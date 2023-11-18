# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as UA
from django.utils.translation import gettext_lazy as _

from .models import User


@admin.register(User)
class UserAdmin(UA):
    add_form_template = "admin/auth/user/add_form.html"
    change_user_password_template = None
    fieldsets = (
        (None, {"fields": ("phone_number", "password")}),
        (_("Personal info"), {"fields": ("full_name", "email")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "is_doctor",
                    "is_partner",
                    "is_user",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("phone_number", "password1", "password2"),
            },
        ),
    )
    list_display = (
        "full_name",
        "phone_number",
        "verified",
        "is_active",
        "is_admin",
        "is_staff",
        "is_doctor",
        "is_partner",
        "is_user",
    )
    list_filter = ("is_staff", "is_superuser", "is_active", "is_doctor", "groups")
    search_fields = ("phone_number", "full_name")
    ordering = (
        "full_name",
        "phone_number",
    )
    filter_horizontal = (
        "groups",
        "user_permissions",
    )
