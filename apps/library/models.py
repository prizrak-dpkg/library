import binascii
from datetime import date
import os
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from apps.library.validators import CategoryValidator, PublisherValidator, BookValidator
from apps.users.models import User


#############
## library ##
#############


#   =====================   #
#   Table name: BaseModel   #
#   =====================   #
class BaseModel(models.Model):
    id = models.AutoField(
        verbose_name="Primary key (A.I)",
        primary_key=True,
    )
    registration_date = models.DateTimeField(
        verbose_name="Registration date",
        auto_now=False,
        auto_now_add=True,
    )
    modification_date = models.DateTimeField(
        verbose_name="Modification date",
        auto_now=True,
        auto_now_add=False,
    )
    status = models.BooleanField(
        verbose_name="Status for logical elimination",
        default=True,
    )

    class Meta:
        abstract = True


#   ====================   #
#   Table name: Category   #
#   ====================   #
class Category(BaseModel):

    category_validator = CategoryValidator()

    name = models.CharField(
        verbose_name="Category name",
        max_length=50,
        unique=True,
        validators=[category_validator],
        help_text="Category name, 50 characters or fewer. Letters and spaces only.",
        error_messages={
            "unique": "A category with that name already exists.",
        },
    )
    standar_loan = models.PositiveSmallIntegerField(
        verbose_name="Standar loan",
        validators=[
            MinValueValidator(limit_value=7),
            MaxValueValidator(limit_value=30),
        ],
        help_text="Standar loan, a minimum of 7 days and a maximum of 30 days.",
    )
    penalty_payment = models.DecimalField(
        verbose_name="Penalty payment",
        max_digits=7,
        decimal_places=2,
        validators=[
            MinValueValidator(limit_value=500),
            MaxValueValidator(limit_value=10000),
        ],
        default=500,
        help_text=(
            "Penalty payment, a minimum of COP 500.00 per day and a "
            "maximum of COP 10,000.00 per day."
        ),
    )

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return "{}".format(
            self.name,
        )


#   ==================   #
#   Table name: Author   #
#   ==================   #
class Author(BaseModel):
    first_name = models.CharField(
        verbose_name="First name",
        max_length=150,
    )
    last_name = models.CharField(
        verbose_name="Last name",
        max_length=150,
    )

    class Meta:
        verbose_name = "Author"
        verbose_name_plural = "Authors"

    def __str__(self):
        return "{} {}".format(
            self.first_name,
            self.last_name,
        )


#   =====================   #
#   Table name: Publisher   #
#   =====================   #
class Publisher(BaseModel):

    publisher_validator = PublisherValidator()

    name = models.CharField(
        verbose_name="Publisher name",
        max_length=150,
        unique=True,
        validators=[publisher_validator],
        help_text=(
            "Publisher name, between 3 and 150 characters. Letters, digits "
            "and spaces only."
        ),
        error_messages={
            "unique": "A publisher with that name already exists.",
        },
    )

    class Meta:
        verbose_name = "Publisher"
        verbose_name_plural = "Publishers"

    def __str__(self):
        return "{}".format(
            self.name,
        )


#   ================   #
#   Table name: Book   #
#   ================   #
class Book(BaseModel):

    book_validator = BookValidator()
    languages = [
        ("ES", "Español"),
        ("EN", "English"),
    ]

    title = models.CharField(
        verbose_name="Book title",
        max_length=150,
        unique=True,
        validators=[book_validator],
        help_text=(
            "Book title, between 3 and 150 characters. Letters, digits, "
            "spaces, punctuation marks (. , ; : () [] ' \" ¡! ¿?) and "
            "basic mathematical symbols (+ - / * =) only."
        ),
        error_messages={
            "unique": "A book with that title already exists.",
        },
    )
    author = models.ForeignKey(
        verbose_name="Author",
        to=Author,
        on_delete=models.PROTECT,
        related_name="book_author",
    )
    publisher = models.ForeignKey(
        verbose_name="Publisher",
        to=Publisher,
        on_delete=models.PROTECT,
        related_name="book_publisher",
    )
    category = models.ForeignKey(
        verbose_name="Category",
        to=Category,
        on_delete=models.PROTECT,
        related_name="book_category",
    )
    language = models.CharField(
        verbose_name="Language",
        max_length=2,
        choices=languages,
        default="ES",
    )
    number_pages = models.PositiveSmallIntegerField(
        verbose_name="Number of pages",
        validators=[
            MinValueValidator(limit_value=10),
            MaxValueValidator(limit_value=3000),
        ],
        help_text="Number of pages, a minimum of 10 pages and a maximum of 3.000 pages.",
    )
    year_publication = models.PositiveSmallIntegerField(
        verbose_name="Year of publication",
        validators=[
            MinValueValidator(limit_value=1000),
            MaxValueValidator(limit_value=date.today().year),
        ],
        help_text="Year of publication, a minimum of year 1.000 and a maximum of year 3.000.",
    )
    available_units = models.PositiveSmallIntegerField(
        verbose_name="Available units",
        validators=[
            MinValueValidator(limit_value=1),
            MaxValueValidator(limit_value=3000),
        ],
        help_text="Available units, a minimum of 1 units and a maximum of 3.000 units.",
    )

    class Meta:
        verbose_name = "Book"
        verbose_name_plural = "Books"

    def __str__(self):
        return "{}".format(
            self.title,
        )


#   ====================   #
#   Table name: BookLoan   #
#   ====================   #
class BookLoan(models.Model):
    key = models.CharField(
        verbose_name="Key",
        max_length=40,
        primary_key=True,
    )
    registration_date = models.DateTimeField(
        verbose_name="Registration date",
        auto_now=False,
        auto_now_add=True,
    )
    modification_date = models.DateTimeField(
        verbose_name="Modification date",
        auto_now=True,
        auto_now_add=False,
    )
    returned = models.BooleanField(
        verbose_name="The book has been returned",
        default=False,
    )
    user = models.ForeignKey(
        verbose_name="User",
        to=User,
        on_delete=models.PROTECT,
        related_name="bookloan_user",
    )
    book = models.ForeignKey(
        verbose_name="Book",
        to=Book,
        on_delete=models.PROTECT,
        related_name="bookloan_book",
    )

    class Meta:
        verbose_name = "Book loan"
        verbose_name_plural = "Book loans"

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super().save(*args, **kwargs)

    @classmethod
    def generate_key(cls):
        return binascii.hexlify(os.urandom(20)).decode()

    def __str__(self):
        return "{}".format(
            self.key,
        )


#   ================   #
#   Table name: Debt   #
#   ================   #
class Debt(models.Model):
    id = models.AutoField(
        verbose_name="Primary key (A.I)",
        primary_key=True,
    )
    book_loan = models.OneToOneField(
        verbose_name="Book loan",
        to=BookLoan,
        on_delete=models.PROTECT,
        related_name="bookloan_user",
    )
    value_paid = models.DecimalField(
        verbose_name="Value paid",
        max_digits=9,
        decimal_places=2,
        validators=[
            MinValueValidator(limit_value=500),
            MaxValueValidator(limit_value=1000000),
        ],
        default=0,
        help_text=(
            "Value paid for penalty, a minimum of COP 500.00 and a"
            "maximum of COP 1,000,000.00."
        ),
    )
    debt_paid_off = models.BooleanField(
        verbose_name="Debt paid off",
        default=False,
    )

    class Meta:
        verbose_name = "Debt"
        verbose_name_plural = "Debts"

    def __str__(self):
        return "{}".format(
            self.book_loan.user,
        )
