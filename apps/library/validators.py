from django.core import validators
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _


@deconstructible
class CategoryValidator(validators.RegexValidator):
    regex = r"^[a-z A-záéíóúñ]{3,50}$"
    message = _(
        "Enter a valid category name. This value may contain only letters "
        "and spaces, between 3 and 50 characters."
    )
    flags = 0


@deconstructible
class PublisherValidator(validators.RegexValidator):
    regex = r"^[\w áéíóú]{3,150}$"
    message = _(
        "Enter a valid publisher name. This value may contain only letters, "
        "numbers and spaces, between 3 and 150 characters."
    )
    flags = 0


@deconstructible
class BookValidator(validators.RegexValidator):
    regex = r"^[\w.áéíóúñ,;: ()[\]¡!'\"¿?*/+-=]{3,150}$"
    message = _(
        "Enter a valid book name. This value may contain only letters, "
        "numbers, spaces, punctuation marks (. , ; : () [] ' \" ¡! ¿?) "
        "and basic mathematical symbols (+ - / * =), between 3 and 150 "
        "characters."
    )
    flags = 0
