# Generated by Django 4.1.1 on 2022-09-28 21:11

import apps.library.validators
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Author",
            fields=[
                (
                    "id",
                    models.AutoField(
                        primary_key=True,
                        serialize=False,
                        verbose_name="Primary key (A.I)",
                    ),
                ),
                (
                    "registration_date",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Registration date"
                    ),
                ),
                (
                    "modification_date",
                    models.DateTimeField(
                        auto_now=True, verbose_name="Modification date"
                    ),
                ),
                (
                    "status",
                    models.BooleanField(
                        default=True, verbose_name="Status for logical elimination"
                    ),
                ),
                (
                    "first_name",
                    models.CharField(max_length=150, verbose_name="First name"),
                ),
                (
                    "last_name",
                    models.CharField(max_length=150, verbose_name="Last name"),
                ),
            ],
            options={
                "verbose_name": "Author",
                "verbose_name_plural": "Authors",
            },
        ),
        migrations.CreateModel(
            name="Book",
            fields=[
                (
                    "id",
                    models.AutoField(
                        primary_key=True,
                        serialize=False,
                        verbose_name="Primary key (A.I)",
                    ),
                ),
                (
                    "registration_date",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Registration date"
                    ),
                ),
                (
                    "modification_date",
                    models.DateTimeField(
                        auto_now=True, verbose_name="Modification date"
                    ),
                ),
                (
                    "status",
                    models.BooleanField(
                        default=True, verbose_name="Status for logical elimination"
                    ),
                ),
                (
                    "title",
                    models.CharField(
                        error_messages={
                            "unique": "A book with that title already exists."
                        },
                        help_text="Book title, between 3 and 150 characters. Letters, digits, spaces, punctuation marks (. , ; : () [] ' \" ¡! ¿?) and basic mathematical symbols (+ - / * =) only.",
                        max_length=150,
                        unique=True,
                        validators=[apps.library.validators.BookValidator()],
                        verbose_name="Book title",
                    ),
                ),
                (
                    "language",
                    models.CharField(
                        choices=[("ES", "Español"), ("EN", "English")],
                        default="ES",
                        max_length=2,
                        verbose_name="Language",
                    ),
                ),
                (
                    "number_pages",
                    models.PositiveSmallIntegerField(
                        help_text="Number of pages, a minimum of 10 pages and a maximum of 3.000 pages.",
                        validators=[
                            django.core.validators.MinValueValidator(limit_value=10),
                            django.core.validators.MaxValueValidator(3000),
                        ],
                        verbose_name="Number of pages",
                    ),
                ),
                (
                    "year_publication",
                    models.PositiveSmallIntegerField(
                        help_text="Year of publication, a minimum of year 1.000 and a maximum of year 3.000.",
                        validators=[
                            django.core.validators.MinValueValidator(limit_value=1000),
                            django.core.validators.MaxValueValidator(3000),
                        ],
                        verbose_name="Year of publication",
                    ),
                ),
                (
                    "available_units",
                    models.PositiveSmallIntegerField(
                        help_text="Available units, a minimum of 1 units and a maximum of 3.000 units.",
                        validators=[
                            django.core.validators.MinValueValidator(limit_value=1),
                            django.core.validators.MaxValueValidator(3000),
                        ],
                        verbose_name="Available units",
                    ),
                ),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="book_author",
                        to="library.author",
                        verbose_name="Author",
                    ),
                ),
            ],
            options={
                "verbose_name": "Book",
                "verbose_name_plural": "Books",
            },
        ),
        migrations.CreateModel(
            name="BookLoan",
            fields=[
                (
                    "key",
                    models.CharField(
                        max_length=40,
                        primary_key=True,
                        serialize=False,
                        verbose_name="Key",
                    ),
                ),
                (
                    "registration_date",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Registration date"
                    ),
                ),
                (
                    "modification_date",
                    models.DateTimeField(
                        auto_now=True, verbose_name="Modification date"
                    ),
                ),
                (
                    "returned",
                    models.BooleanField(
                        default=False, verbose_name="The book has been returned"
                    ),
                ),
                (
                    "book",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="bookloan_book",
                        to="library.book",
                        verbose_name="Book",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="bookloan_user",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="User",
                    ),
                ),
            ],
            options={
                "verbose_name": "Book loan",
                "verbose_name_plural": "Book loans",
                "ordering": ["registration_date"],
            },
        ),
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.AutoField(
                        primary_key=True,
                        serialize=False,
                        verbose_name="Primary key (A.I)",
                    ),
                ),
                (
                    "registration_date",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Registration date"
                    ),
                ),
                (
                    "modification_date",
                    models.DateTimeField(
                        auto_now=True, verbose_name="Modification date"
                    ),
                ),
                (
                    "status",
                    models.BooleanField(
                        default=True, verbose_name="Status for logical elimination"
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        error_messages={
                            "unique": "A category with that name already exists."
                        },
                        help_text="Category name, 50 characters or fewer. Letters and spaces only.",
                        max_length=50,
                        unique=True,
                        validators=[apps.library.validators.CategoryValidator()],
                        verbose_name="Category name",
                    ),
                ),
                (
                    "standar_loan",
                    models.PositiveSmallIntegerField(
                        help_text="Standar loan, a minimum of 7 days and a maximum of 30 days.",
                        validators=[
                            django.core.validators.MinValueValidator(limit_value=5),
                            django.core.validators.MaxValueValidator(30),
                        ],
                        verbose_name="Standar loan",
                    ),
                ),
                (
                    "penalty_payment",
                    models.DecimalField(
                        decimal_places=2,
                        default=500,
                        help_text="Penalty payment, a minimum of COP 500,00 per day and a maximum of COP 10.000,00 per day.",
                        max_digits=7,
                        validators=[
                            django.core.validators.MinValueValidator(limit_value=500),
                            django.core.validators.MaxValueValidator(10000),
                        ],
                        verbose_name="Penalty payment",
                    ),
                ),
            ],
            options={
                "verbose_name": "Category",
                "verbose_name_plural": "Categories",
            },
        ),
        migrations.CreateModel(
            name="Publisher",
            fields=[
                (
                    "id",
                    models.AutoField(
                        primary_key=True,
                        serialize=False,
                        verbose_name="Primary key (A.I)",
                    ),
                ),
                (
                    "registration_date",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Registration date"
                    ),
                ),
                (
                    "modification_date",
                    models.DateTimeField(
                        auto_now=True, verbose_name="Modification date"
                    ),
                ),
                (
                    "status",
                    models.BooleanField(
                        default=True, verbose_name="Status for logical elimination"
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        error_messages={
                            "unique": "A publisher with that name already exists."
                        },
                        help_text="Publisher name, between 3 and 150 characters. Letters, digits and spaces only.",
                        max_length=150,
                        unique=True,
                        validators=[apps.library.validators.PublisherValidator()],
                        verbose_name="Publisher name",
                    ),
                ),
            ],
            options={
                "verbose_name": "Publisher",
                "verbose_name_plural": "Publishers",
            },
        ),
        migrations.CreateModel(
            name="Debt",
            fields=[
                (
                    "id",
                    models.AutoField(
                        primary_key=True,
                        serialize=False,
                        verbose_name="Primary key (A.I)",
                    ),
                ),
                (
                    "book_loan",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="bookloan_user",
                        to="library.bookloan",
                        verbose_name="Book loan",
                    ),
                ),
            ],
            options={
                "verbose_name": "Debt",
                "verbose_name_plural": "Debts",
                "ordering": ["book_loan__user__document_number"],
            },
        ),
        migrations.AddField(
            model_name="book",
            name="category",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="book_category",
                to="library.category",
                verbose_name="Category",
            ),
        ),
        migrations.AddField(
            model_name="book",
            name="publisher",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="book_publisher",
                to="library.publisher",
                verbose_name="Publisher",
            ),
        ),
    ]
