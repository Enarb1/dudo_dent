from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm

from dudo_dent.accounts.forms import CustomUserCreationBaseForm

# Register your models here.

UserModel = get_user_model()

@admin.register(UserModel)
class CustomUserAdmin(UserAdmin):
    model = UserModel
    add_form = CustomUserCreationBaseForm
    form = UserChangeForm

    list_display = ("email", "full_name", "is_staff")
    list_filter = ("is_staff", "is_superuser", "is_active", "groups")
    search_fields = ("full_name", "email")
    ordering = ("pk",)

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (("Personal info"), {"fields": ("full_name",)}),
        (("Permissions"),{"fields": ("is_active", "is_staff","groups","user_permissions")}),
        (("Important dates"), {"fields": ("last_login", )}),
    )
    add_fieldsets = (
        (None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )

