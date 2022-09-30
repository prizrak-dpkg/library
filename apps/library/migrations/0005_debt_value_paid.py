# Generated by Django 4.1.1 on 2022-09-30 15:33

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("library", "0004_alter_debt_book_loan"),
    ]

    operations = [
        migrations.AddField(
            model_name="debt",
            name="value_paid",
            field=models.DecimalField(
                decimal_places=2,
                default=0,
                help_text="Value paid for penalty, a minimum of COP 500,00 and amaximum of COP 1.000.000,00.",
                max_digits=9,
                validators=[
                    django.core.validators.MinValueValidator(limit_value=500),
                    django.core.validators.MaxValueValidator(limit_value=1000000),
                ],
                verbose_name="Value paid",
            ),
        ),
    ]
