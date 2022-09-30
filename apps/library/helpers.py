from ctypes import Union
from datetime import date
import math
import re
from django.contrib.auth.models import Group
from django.core import exceptions
from django.core.paginator import Paginator
from django.shortcuts import render
from django.views.generic import TemplateView

from apps.library.models import Author, Book, BookLoan, Category, Debt, Publisher
from apps.users.models import User


class BaseView(TemplateView):
    number_of_results_per_page = 10
    dictionary_in_response = {}
    query = []

    def get(self, request, *args, **kwargs):
        results = len(self.query)
        current_page = request.GET.get("page")
        paginator = Paginator(self.query, self.number_of_results_per_page)
        info = paginator.get_page(current_page)
        self.dictionary_in_response.update(
            {
                "info": info,
                "number_of_results": math.ceil(
                    results / self.number_of_results_per_page
                ),
            }
        )
        return render(
            request,
            self.template_name,
            self.dictionary_in_response,
        )


class GeneralValidations:
    def remove_excess_whitespace(self, string, uppercase=False):
        whitespace_regex = re.compile(r"(\s)+")
        fstring = re.sub(whitespace_regex, " ", string).strip()
        if uppercase:
            return fstring.upper()
        return fstring.title()

    def get_currency(self, value):
        return f"COP {value:,.2f}"

    def validate_words(self, string, start, end):
        regex = "^[a-z A-záéíóúñ]{" + f"{start},{end}" + "}$"
        words_regex = re.compile(rf"{regex}")
        return words_regex.search(string) is not None

    def validate_text(self, string, start, end):
        regex = "^[\w.áéíóúñ,;: ()[\]¡!'\"¿?*/+-=]{" + f"{start},{end}" + "}$"
        text_regex = re.compile(rf"{regex}")
        return text_regex.search(string) is not None

    def validate_digit(self, string, start, end):
        regex = "^[1-9]{1\}[\d]{" + f"{start},{end}" + "}$"
        text_regex = re.compile(rf"{regex}")
        return text_regex.search(string) is not None

    def validate_min(self, value, min):
        try:
            value = float(value)
            if value < min:
                return False
            return True
        except:
            return False

    def validate_max(self, value, max):
        try:
            value = float(value)
            if value > max:
                return False
            return True
        except:
            return False

    def validate_debt_paid_off(self, user):
        if (
            Debt.objects.filter(book_loan__user=user, debt_paid_off=False)
            .only("id")
            .exists()
        ):
            return False
        return True

    def validate_loans(self, user):
        loans = BookLoan.objects.filter(user=user, returned=False).only(
            "key",
            "registration_date",
            "modification_date",
            "book",
        )
        for loan in loans:
            days_elapsed = date.today() - loan.registration_date.date()
            if days_elapsed.days > loan.book.category.standar_loan:
                debt = Debt.objects.filter(book_loan=loan).values("id").first()
                if debt is None:
                    debt = Debt(book_loan=loan)
                    debt.save()

    def validate_debs(self, registration_date, standar_loan, penalty_payment):
        days_elapsed = date.today() - registration_date.date()
        if days_elapsed.days > standar_loan:
            return (days_elapsed.days - standar_loan) * penalty_payment
        return 0

    def validate_category(self, data):
        errors = []
        if not self.validate_words(data["name"], 3, 50):
            errors.append(
                {
                    "field": "Categoría",
                    "error": "Sólo puede contener letras y espacios, entre 3 y 50 caracteres.",
                }
            )

        if not self.validate_min(data["standar_loan"], 7) or not self.validate_max(
            data["standar_loan"], 30
        ):
            errors.append(
                {
                    "field": "Días de prestamo",
                    "error": "Un mínimo de 7 días y un máximo de 30 días.",
                }
            )
        if not self.validate_min(data["penalty_payment"], 500) or not self.validate_max(
            data["penalty_payment"], 10000
        ):
            errors.append(
                {
                    "field": "Penalidad diaria",
                    "error": "Un mínimo de COP 500.00 por día y un máximo de COP 10,000.00 por día.",
                }
            )
        return errors

    def validate_book(self, data):
        errors = []
        if not self.validate_text(data["title"], 3, 150):
            errors.append(
                {
                    "field": "Título",
                    "error": "Sólo puede contener letras, números, espacios, signos de puntuación (. , ; : () [] ' \" ¡! ¿?) y símbolos matemáticos básicos (+ - / * =), entre 3 y 150 caracteres.",
                }
            )

        if not data["author"] == "":
            if (
                Author.objects.filter(status=True, id=data["author"])
                .values("id")
                .first()
                is None
            ):
                errors.append(
                    {
                        "field": "Autor",
                        "error": "Autor no encontrado.",
                    }
                )
        else:
            errors.append(
                {
                    "field": "Autor",
                    "error": "Debe seleccionar un autor.",
                }
            )
        if not data["publisher"] == "":
            if (
                Publisher.objects.filter(status=True, id=data["publisher"])
                .values("id")
                .first()
                is None
            ):
                errors.append(
                    {
                        "field": "Editorial",
                        "error": "Editorial no encontrado.",
                    }
                )
        else:
            errors.append(
                {
                    "field": "Editorial",
                    "error": "Debe seleccionar una editorial.",
                }
            )
        if not data["category"] == "":
            if (
                Category.objects.filter(status=True, id=data["category"])
                .values("id")
                .first()
                is None
            ):
                errors.append(
                    {
                        "field": "Categoría",
                        "error": "Categoría no encontrado.",
                    }
                )
        else:
            errors.append(
                {
                    "field": "Categoría",
                    "error": "Debe seleccionar una categoría.",
                }
            )
        if not data["language"] in [x[0] for x in Book.languages]:
            errors.append(
                {
                    "field": "Idioma",
                    "error": "Idioma no encontrado.",
                }
            )
        if not self.validate_min(data["number_pages"], 10) or not self.validate_max(
            data["number_pages"], 3000
        ):
            errors.append(
                {
                    "field": "Número de páginas",
                    "error": "Un mínimo de 10 páginas y un máximo de 3.000 páginas.",
                }
            )
        if not self.validate_min(data["year_publication"], 10) or not self.validate_max(
            data["year_publication"], date.today().year
        ):
            errors.append(
                {
                    "field": "Año de publicación",
                    "error": f"Como mínimo el año 1000 y como máximo el año {date.today().year}.",
                }
            )
        if not self.validate_min(data["available_units"], 1) or not self.validate_max(
            data["available_units"], 3000
        ):
            errors.append(
                {
                    "field": "Unidades disponibles",
                    "error": "Como mínimo 1 unidad y como máximo 3.000 unidades.",
                }
            )
        return errors

    def validate_bookloan(self, data):
        errors = []
        if not data["document_number"] == "":
            user = (
                User.objects.filter(
                    is_active=True, document_number=data["document_number"]
                )
                .only("id")
                .first()
            )
            if user is not None:
                if (
                    BookLoan.objects.filter(user=user, returned=False)
                    .only("key")
                    .exists()
                ):
                    self.validate_loans(user=user)
                if not self.validate_debt_paid_off(user=user):
                    errors.append(
                        {
                            "field": "Documento",
                            "error": "El usuario tiene sanciones por demora en la entrega de libros. Debe saldar la multa impuesta antes de solicitar otro préstamo.",
                        }
                    )
            else:
                errors.append(
                    {
                        "field": "Documento",
                        "error": "No se han encontrado usuarios con el documento proporcionado.",
                    }
                )

        else:
            errors.append(
                {
                    "field": "Documento",
                    "error": "No puede estar vacío.",
                }
            )
        return errors

    def validate_user_bookloan(self, data):
        errors = []
        if not data["document_number"] == "":
            user = (
                User.objects.filter(
                    is_active=True, document_number=data["document_number"]
                )
                .only("id")
                .first()
            )
            if user is not None:
                if (
                    BookLoan.objects.filter(user=user, returned=False)
                    .only("key")
                    .exists()
                ):
                    self.validate_loans(user=user)
            else:
                errors.append(
                    {
                        "field": "Documento",
                        "error": "No se han encontrado usuarios con el documento proporcionado.",
                    }
                )

        else:
            errors.append(
                {
                    "field": "Documento",
                    "error": "No puede estar vacío.",
                }
            )
        return errors

    def validate_user(self, data, new=True):
        errors = []
        if not self.validate_digit(data["document_number"], 6, 10):
            errors.append(
                {
                    "field": "Documento",
                    "error": f"Sólo puede contener letras y espacios, entre 3 y 50 caracteres.",
                }
            )
        return errors

    class Meta:
        abstract = True
