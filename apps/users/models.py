from django.contrib.auth.models import AbstractUser
from django.db import models
from apps.users.validators import AddressValidator, DocumentValidator, PhoneValidator


###########
## Users ##
###########


#   ================   #
#   Table name: User   #
#   ================   #
class User(AbstractUser):

    address_validator = AddressValidator()
    phone_validator = PhoneValidator()
    document_validator = DocumentValidator()

    document_number = models.CharField(
        verbose_name="Document number",
        unique=True,
        max_length=10,
        validators=[document_validator],
        help_text="Required. Digits only.",
        error_messages={
            "unique": "A user with that document number already exists.",
        },
    )
    email = models.EmailField(
        verbose_name="E-mail address",
        unique=True,
        help_text="Required. Format: username@domain.",
        error_messages={
            "unique": "A user with that email already exists.",
        },
    )
    address = models.CharField(
        verbose_name="Address",
        max_length=100,
        validators=[address_validator],
        help_text=(
            "Required. Residence address, 100 characters or fewer. "
            "Letters, digits and #/- only."
        ),
    )
    phone = models.CharField(
        verbose_name="Phone",
        max_length=10,
        validators=[phone_validator],
        help_text="Required. Phone number, between 7 and 10 characters. Digits only.",
    )
    is_librarian = models.BooleanField(
        verbose_name="Librarian",
        default=False,
        help_text="Designates whether the user belongs to the authorized library staff.",
    )
    USERNAME_FIELD = "document_number"
    REQUIRED_FIELDS = [
        "username",
        "first_name",
        "last_name",
        "email",
        "address",
        "phone",
    ]

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return "{}".format(
            self.username,
        )
