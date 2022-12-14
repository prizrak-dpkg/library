# Generated by Django 4.1.1 on 2022-09-28 17:05

import apps.users.validators
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                (
                    "username",
                    models.CharField(
                        error_messages={
                            "unique": "A user with that username already exists."
                        },
                        help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
                        max_length=150,
                        unique=True,
                        validators=[
                            django.contrib.auth.validators.UnicodeUsernameValidator()
                        ],
                        verbose_name="username",
                    ),
                ),
                (
                    "first_name",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="first name"
                    ),
                ),
                (
                    "last_name",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="last name"
                    ),
                ),
                (
                    "is_staff",
                    models.BooleanField(
                        default=False,
                        help_text="Designates whether the user can log into this admin site.",
                        verbose_name="staff status",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True,
                        help_text="Designates whether this user should be treated as active. Unselect this instead of deleting accounts.",
                        verbose_name="active",
                    ),
                ),
                (
                    "date_joined",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="date joined"
                    ),
                ),
                (
                    "document_number",
                    models.CharField(
                        error_messages={
                            "unique": "A user with that document number already exists."
                        },
                        help_text="Required. Digits only.",
                        max_length=10,
                        unique=True,
                        validators=[apps.users.validators.DocumentValidator()],
                        verbose_name="Document number",
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        error_messages={
                            "unique": "A user with that email already exists."
                        },
                        help_text="Required. Format: username@domain.",
                        max_length=254,
                        unique=True,
                        verbose_name="E-mail address",
                    ),
                ),
                (
                    "address",
                    models.CharField(
                        help_text="Required. Residence address, 100 characters or fewer. Letters, digits and #/- only.",
                        max_length=100,
                        validators=[apps.users.validators.AddressValidator()],
                        verbose_name="Address",
                    ),
                ),
                (
                    "phone",
                    models.CharField(
                        help_text="Required. Phone number, between 7 and 10 characters. Digits only.",
                        max_length=10,
                        validators=[apps.users.validators.PhoneValidator()],
                        verbose_name="Phone",
                    ),
                ),
                (
                    "status",
                    models.BooleanField(
                        default=False, verbose_name="Status for sanction"
                    ),
                ),
                (
                    "profile_image",
                    models.ImageField(
                        default="assets/images/library.png",
                        upload_to="profile/",
                        verbose_name="Profile image",
                    ),
                ),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "verbose_name": "User",
                "verbose_name_plural": "Users",
                "ordering": ["last_name"],
            },
            managers=[
                ("objects", django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
