from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as UserBaseAdmin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from apps.users.models import *


###########
## Users ##
###########


#   ================   #
#   Table name: User   #
#   ================   #
class UserResource(resources.ModelResource):
    class Meta:
        model = User


class UserAdmin(UserBaseAdmin, ImportExportModelAdmin, admin.ModelAdmin):
    fieldsets = (
        (None, {"fields": ("document_number", "username", "password")}),
        (
            ("Personal info"),
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                    "address",
                    "phone",
                )
            },
        ),
        (
            ("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "is_librarian",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "document_number", "password1", "password2"),
            },
        ),
    )
    search_fields = [
        "document_number",
        "email",
    ]
    list_display = (
        "id",
        "date_joined",
        "last_login",
        "is_superuser",
        "is_staff",
        "is_active",
        "is_librarian",
        "username",
        "document_number",
        "first_name",
        "last_name",
        "email",
        "address",
        "phone",
    )
    resource_class = UserResource


admin.site.register(
    User,
    UserAdmin,
)
