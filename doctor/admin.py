# Register your models here.
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Doctor


@admin.register(Doctor)
class UserAdmin(admin.ModelAdmin):
    pass
    # fieldsets = (
    #     (None, {"fields": ("phone_number", "password")}),
    #     (_("Personal info"), {"fields": ("full_name", "email")}),
    #     (
    #         _("Permissions"),
    #         {
    #             "fields": (
    #                 "is_active",
    #                 "is_staff",
    #                 "is_superuser",
    #                 "groups",
    #                 "user_permissions",
    #             ),
    #         },
    #     ),
    #     (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    # )
    # add_fieldsets = (
    #     (
    #         None,
    #         {
    #             "classes": ("wide",),
    #             "fields": ("phone_number", "password1", "password2"),
    #         },
    #     ),
    # )
    # list_display = ("phone_number", "email", "full_name", "is_staff")
    # list_filter = ("is_staff", "is_superuser", "is_active", "groups")
    # search_fields = ("phone_number", "full_name", "email")
    # ordering = ("phone_number",)
    # filter_horizontal = (
    #     "groups",
    #     "user_permissions",
    # )
