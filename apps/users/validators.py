from django.core import validators
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _


@deconstructible
class AddressValidator(validators.RegexValidator):
    regex = r"^[\w #-]+$"
    message = _(
        "Enter a valid address. This value may contain only letters, "
        "numbers, spaces, and #/- characters."
    )
    flags = 0


@deconstructible
class DocumentValidator(validators.RegexValidator):
    regex = r"^[1-9]{1}[\d]{5,10}$"
    message = _(
        "Enter a valid document number. This value may contain only digits, "
        "between 6 and 10 characters."
    )
    flags = 0


@deconstructible
class PhoneValidator(validators.RegexValidator):
    regex = r"^[1-9]{1}[\d]{6,10}$"
    message = _(
        "Enter a valid phone. This value may contain only digits, "
        "between 7 and 10 characters."
    )
    flags = 0
