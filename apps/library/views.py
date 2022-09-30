from functools import reduce
import json
import random
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http.response import HttpResponse
from apps.library.helpers import BaseView, GeneralValidations
from apps.library.models import Author, Book, BookLoan, Category, Debt, Publisher
from apps.users.models import User


class AdminRequest(LoginRequiredMixin, BaseView):
    template_name = "admin/admin.html"

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class CategoryRequest(LoginRequiredMixin, BaseView, GeneralValidations):
    template_name = "admin/category.html"
    model = Category

    def get(self, request, *args, **kwargs):
        self.number_of_results_per_page = 5
        search = request.GET.get("search")
        categories = (
            self.model.objects.filter(status=True).values("id", "name")
            if search == None
            else self.model.objects.filter(
                Q(name__icontains=search),
                Q(status=True),
            )
            .values("id", "name")
            .distinct()
        )
        self.query = [*categories]
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if request.POST.get("get_category"):
            data = json.loads(request.POST.get("get_category"))
            category = (
                self.model.objects.filter(id=data["id"])
                .values("name", "standar_loan", "penalty_payment")
                .first()
            )
            if category is not None:
                server_response = {
                    "response": True,
                    "data": {
                        "id": data["id"],
                        "name": category["name"],
                        "standar_loan": category["standar_loan"],
                        "penalty_payment": f'{category["penalty_payment"]}',
                    },
                    "status": 200,
                }
            else:
                server_response = {
                    "response": False,
                    "detail": "Bad Request",
                    "status": 400,
                }
        elif request.POST.get("create_category"):
            data = json.loads(request.POST.get("create_category"))
            data.update({"name": self.remove_excess_whitespace(data["name"])})
            errors = self.validate_category(data)
            if not errors:
                category = self.model(
                    name=data["name"],
                    standar_loan=data["standar_loan"],
                    penalty_payment=data["penalty_payment"],
                )
                category.save()
                server_response = {
                    "response": True,
                    "redirect": "/library/category/",
                    "status": 200,
                }
            else:
                server_response = {
                    "response": False,
                    "detail": errors,
                    "status": 400,
                }
        elif request.POST.get("update_category"):
            data = json.loads(request.POST.get("update_category"))
            data.update({"name": self.remove_excess_whitespace(data["name"])})
            errors = self.validate_category(data)
            if not errors:
                category = self.model.objects.get(id=data["id"])
                category.name = data["name"]
                category.standar_loan = data["standar_loan"]
                category.penalty_payment = data["penalty_payment"]
                category.save()
                server_response = {
                    "response": True,
                    "redirect": "/library/category/",
                    "status": 200,
                }
            else:
                server_response = {
                    "response": False,
                    "detail": errors,
                    "status": 400,
                }
        elif request.POST.get("delete_category"):
            data = json.loads(request.POST.get("delete_category"))
            category = self.model.objects.filter(id=data["id"]).only("id").first()
            if category is not None:
                if Book.objects.filter(category=category).only("id").exists():
                    server_response = {
                        "response": False,
                        "detail": [
                            {
                                "field": "Categoría",
                                "error": "No podemos eliminar la Categoría, ya que tiene Libros asociados.",
                            }
                        ],
                        "status": 400,
                    }
                else:
                    category.delete()
                    server_response = {
                        "response": True,
                        "redirect": "/library/category/",
                        "status": 200,
                    }
            else:
                server_response = {
                    "response": True,
                    "redirect": "/library/category/",
                    "status": 200,
                }
        else:
            server_response = {
                "response": False,
                "detail": "Bad Request",
                "status": 400,
            }
        return HttpResponse(json.dumps(server_response))


class BookRequest(LoginRequiredMixin, BaseView, GeneralValidations):
    template_name = "admin/book.html"
    model = Book

    def get(self, request, *args, **kwargs):
        self.number_of_results_per_page = 5
        search = request.GET.get("search")
        books = (
            self.model.objects.filter(status=True).values("id", "title")
            if search == None
            else self.model.objects.filter(
                Q(title__icontains=search),
                Q(status=True),
            )
            .values("id", "title")
            .distinct()
        )
        self.query = [*books]
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if request.POST.get("get_book_options"):
            author, publisher, category, language = self.book_options
            server_response = {
                "response": True,
                "data": {
                    "author_options": author,
                    "publisher_options": publisher,
                    "category_options": category,
                    "language_options": language,
                },
                "status": 200,
            }
        elif request.POST.get("get_book"):
            data = json.loads(request.POST.get("get_book"))
            book = (
                self.model.objects.filter(id=data["id"])
                .values(
                    "title",
                    "author__id",
                    "publisher__id",
                    "category__id",
                    "language",
                    "number_pages",
                    "year_publication",
                    "available_units",
                )
                .first()
            )
            if book is not None:
                author, publisher, category, language = self.book_options
                server_response = {
                    "response": True,
                    "data": {
                        "id": data["id"],
                        "title": book["title"],
                        "author": book["author__id"],
                        "author_options": author,
                        "publisher": book["publisher__id"],
                        "publisher_options": publisher,
                        "category": book["category__id"],
                        "category_options": category,
                        "language": book["language"],
                        "language_options": language,
                        "number_pages": book["number_pages"],
                        "year_publication": book["year_publication"],
                        "available_units": book["available_units"],
                    },
                    "status": 200,
                }
            else:
                server_response = {
                    "response": False,
                    "detail": "Bad Request",
                    "status": 400,
                }
        elif request.POST.get("create_book"):
            data = json.loads(request.POST.get("create_book"))
            data.update({"title": self.remove_excess_whitespace(data["title"])})
            errors = self.validate_book(data)
            if not errors:
                book = self.model(
                    title=data["title"],
                    author=Author.objects.get(id=data["author"]),
                    publisher=Publisher.objects.get(id=data["publisher"]),
                    category=Category.objects.get(id=data["category"]),
                    language=data["language"],
                    number_pages=data["number_pages"],
                    year_publication=data["year_publication"],
                    available_units=data["available_units"],
                )
                book.save()
                server_response = {
                    "response": True,
                    "redirect": "/library/book/",
                    "status": 200,
                }
            else:
                server_response = {
                    "response": False,
                    "detail": errors,
                    "status": 400,
                }
        elif request.POST.get("update_book"):
            data = json.loads(request.POST.get("update_book"))
            data.update({"title": self.remove_excess_whitespace(data["title"])})
            errors = self.validate_book(data)
            if not errors:
                book = self.model.objects.get(id=data["id"])
                book.title = data["title"]
                book.author = Author.objects.get(id=data["author"])
                book.publisher = Publisher.objects.get(id=data["publisher"])
                book.category = Category.objects.get(id=data["category"])
                book.language = data["language"]
                book.number_pages = data["number_pages"]
                book.year_publication = data["year_publication"]
                book.available_units = data["available_units"]
                book.save()
                server_response = {
                    "response": True,
                    "redirect": "/library/book/",
                    "status": 200,
                }
            else:
                server_response = {
                    "response": False,
                    "detail": errors,
                    "status": 400,
                }
        elif request.POST.get("delete_book"):
            data = json.loads(request.POST.get("delete_book"))
            book = self.model.objects.filter(id=data["id"]).only("id").first()
            if book is not None:
                if BookLoan.objects.filter(book=book).only("id").exists():
                    server_response = {
                        "response": False,
                        "detail": [
                            {
                                "field": "Libro",
                                "error": "No podemos eliminar el Libro, ya que tiene Préstamos asociados.",
                            }
                        ],
                        "status": 400,
                    }
                else:
                    book.delete()
                    server_response = {
                        "response": True,
                        "redirect": "/library/book/",
                        "status": 200,
                    }
            else:
                server_response = {
                    "response": True,
                    "redirect": "/library/book/",
                    "status": 200,
                }
        else:
            server_response = {
                "response": False,
                "detail": "Bad Request",
                "status": 400,
            }
        return HttpResponse(json.dumps(server_response))

    @property
    def book_options(self):
        author = [
            {"id": x["id"], "name": f'{x["first_name"]} {x["last_name"]}'}
            for x in Author.objects.filter(status=True).values(
                "id", "first_name", "last_name"
            )
        ]
        publisher = Publisher.objects.filter(status=True).values("id", "name")
        category = Category.objects.filter(status=True).values("id", "name")
        language = [{"id": x[0], "name": x[1]} for x in Book.languages]
        return [author, [*publisher], [*category], language]


class BookLoanRequest(LoginRequiredMixin, BaseView, GeneralValidations):
    template_name = "admin/bookloan.html"
    model = Book

    def get(self, request, *args, **kwargs):
        self.number_of_results_per_page = 5
        search = request.GET.get("search")
        books = (
            self.model.objects.filter(status=True).values("id", "title")
            if search == None
            else self.model.objects.filter(
                Q(title__icontains=search),
                Q(status=True),
            )
            .values("id", "title")
            .distinct()
        )
        self.query = [*books]
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if request.POST.get("get_bookloan"):
            data = json.loads(request.POST.get("get_bookloan"))
            book = (
                self.model.objects.filter(id=data["id"])
                .only("id", "title", "author", "available_units")
                .first()
            )
            if book is not None:
                server_response = {
                    "response": True,
                    "data": {
                        "id": data["id"],
                        "title": book.title,
                        "author": f"{book.author.first_name} {book.author.last_name}",
                        "available_units": self.available_units(book=book),
                    },
                    "status": 200,
                }
            else:
                server_response = {
                    "response": False,
                    "detail": "Bad Request",
                    "status": 400,
                }
        elif request.POST.get("book_loan"):
            data = json.loads(request.POST.get("book_loan"))
            errors = self.validate_bookloan(data)
            if not errors:
                book = self.model.objects.filter(id=data["book"]).only("id").first()
                if self.available_units(book=book) > 0:
                    bookloan = BookLoan(
                        user=User.objects.get(document_number=data["document_number"]),
                        book=book,
                    )
                    bookloan.save()
                    server_response = {
                        "response": True,
                        "redirect": "/library/bookloan/",
                        "status": 200,
                    }
                else:
                    errors.append(
                        {
                            "field": "Libro",
                            "error": "No hay unidades disponibles para préstamo.",
                        }
                    )
                    server_response = {
                        "response": False,
                        "detail": errors,
                        "status": 400,
                    }
            else:
                server_response = {
                    "response": False,
                    "detail": errors,
                    "status": 400,
                }
        elif request.POST.get("user_book_loans"):
            data = json.loads(request.POST.get("user_book_loans"))
            errors = self.validate_user_bookloan(data)
            if not errors:
                user = User.objects.get(document_number=data["document_number"])
                book_loan_options = [
                    {"id": x["key"], "name": x["book__title"]}
                    for x in BookLoan.objects.filter(returned=False, user=user).values(
                        "key", "book__title"
                    )
                ]
                server_response = {
                    "response": True,
                    "data": {
                        "book_loan_options": book_loan_options,
                    },
                    "status": 200,
                }
            else:
                server_response = {
                    "response": False,
                    "detail": errors,
                    "status": 400,
                }
        elif request.POST.get("return_book"):
            data = json.loads(request.POST.get("return_book"))
            book_loan = (
                BookLoan.objects.filter(key=data["key"])
                .only("returned", "user")
                .first()
            )
            if book_loan is not None:
                book_loan.returned = True
                book_loan.save()
                if self.validate_debt_paid_off(user=book_loan.user):
                    server_response = {
                        "response": True,
                        "redirect": "/library/bookloan/",
                        "status": 200,
                    }
                else:
                    server_response = {
                        "response": True,
                        "redirect": f"/library/debt/?search={book_loan.user.document_number}",
                        "status": 200,
                    }
            else:
                server_response = {
                    "response": False,
                    "detail": [
                        {
                            "field": "Libro",
                            "error": "Libro no encontrado.",
                        }
                    ],
                    "status": 400,
                }
        else:
            server_response = {
                "response": False,
                "detail": "Bad Request",
                "status": 400,
            }
        return HttpResponse(json.dumps(server_response))

    def available_units(self, book):
        return (
            book.available_units
            - BookLoan.objects.filter(book=book, returned=False).count()
        )


class DebtRequest(LoginRequiredMixin, BaseView, GeneralValidations):
    template_name = "admin/debt.html"
    model = Debt

    def get(self, request, *args, **kwargs):
        self.number_of_results_per_page = 5
        search = request.GET.get("search")
        debts = (
            self.model.objects.filter(debt_paid_off=False).values(
                "book_loan__user__id",
                "book_loan__user__first_name",
                "book_loan__user__last_name",
            )
            if search == None
            else self.model.objects.filter(
                Q(book_loan__user__document_number__icontains=search),
                Q(debt_paid_off=False),
            )
            .values(
                "book_loan__user__id",
                "book_loan__user__first_name",
                "book_loan__user__last_name",
            )
            .distinct()
        )
        self.query = [*debts]
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if request.POST.get("get_debt"):
            data = json.loads(request.POST.get("get_debt"))
            user = (
                User.objects.filter(id=data["id"])
                .only("id", "first_name", "last_name")
                .first()
            )
            if user is not None:
                debts = [
                    {
                        "key": x["book_loan__key"],
                        "value_paid": "{}".format(
                            self.validate_debs(
                                registration_date=x["book_loan__registration_date"],
                                standar_loan=x[
                                    "book_loan__book__category__standar_loan"
                                ],
                                penalty_payment=x[
                                    "book_loan__book__category__penalty_payment"
                                ],
                            )
                        ),
                    }
                    for x in self.model.objects.filter(
                        book_loan__user=user, debt_paid_off=False
                    ).values(
                        "book_loan__key",
                        "book_loan__registration_date",
                        "book_loan__book__category__standar_loan",
                        "book_loan__book__category__penalty_payment",
                    )
                ]
                debt = self.get_currency(
                    reduce(
                        lambda x, y: {
                            "value_paid": float(x["value_paid"])
                            + float(y["value_paid"])
                        },
                        debts,
                        {"value_paid": 0.00},
                    )["value_paid"]
                )
                server_response = {
                    "response": True,
                    "data": {
                        "debt": debt,
                        "user": f"{user.first_name} {user.last_name}",
                        "penalties": len(debts),
                        "debts": debts,
                    },
                    "status": 200,
                }
            else:
                server_response = {
                    "response": False,
                    "detail": "Bad Request",
                    "status": 400,
                }
        elif request.POST.get("pay_debts"):
            data = json.loads(request.POST.get("pay_debts"))
            if data["debts"]["debts"]:
                for debt in data["debts"]["debts"]:
                    penalty = (
                        Debt.objects.filter(
                            book_loan__key=debt["key"], debt_paid_off=False
                        )
                        .only("debt_paid_off")
                        .first()
                    )
                    if penalty is not None:
                        penalty.debt_paid_off = True
                        penalty.value_paid = debt["value_paid"]
                        penalty.save()
            server_response = {
                "response": True,
                "redirect": "/library/debt/",
                "status": 200,
            }
        else:
            server_response = {
                "response": False,
                "detail": "Bad Request",
                "status": 400,
            }
        return HttpResponse(json.dumps(server_response))


class UserRequest(LoginRequiredMixin, BaseView, GeneralValidations):
    template_name = "admin/user.html"
    model = User

    def get(self, request, *args, **kwargs):
        self.number_of_results_per_page = 5
        search = request.GET.get("search")
        users = (
            self.model.objects.filter(is_librarian=False).values(
                "id",
                "first_name",
                "last_name",
            )
            if search == None
            else self.model.objects.filter(
                Q(document_number__icontains=search),
                Q(is_librarian=False),
            )
            .values(
                "id",
                "first_name",
                "last_name",
            )
            .distinct()
        )
        self.query = [*users]
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if request.POST.get("get_user"):
            data = json.loads(request.POST.get("get_user"))
            user = (
                User.objects.filter(id=data["id"])
                .values(
                    "id",
                    "document_number",
                    "first_name",
                    "last_name",
                    "email",
                    "address",
                    "phone",
                )
                .first()
            )
            if user is not None:
                server_response = {
                    "response": True,
                    "data": {**user},
                    "status": 200,
                }
            else:
                server_response = {
                    "response": False,
                    "detail": "Bad Request",
                    "status": 400,
                }
        elif request.POST.get("create_user"):
            data = json.loads(request.POST.get("create_user"))
            data.update(
                {"first_name": self.remove_excess_whitespace(data["first_name"])}
            )
            data.update({"last_name": self.remove_excess_whitespace(data["last_name"])})
            data.update(
                {"address": self.remove_excess_whitespace(data["address"], True)}
            )
            errors = self.validate_user(data)
            if not errors:
                user = self.model.create_user(
                    username=data["document_number"],
                    email=data["email"],
                    password=self.password_generator(length=15),
                )
                user.document_number = data["document_number"]
                user.first_name = data["first_name"]
                user.last_name = data["last_name"]
                user.address = data["address"]
                user.phone = data["phone"]
                user.save()
                server_response = {
                    "response": True,
                    "redirect": "/library/user/",
                    "status": 200,
                }
            else:
                server_response = {
                    "response": False,
                    "detail": errors,
                    "status": 400,
                }
        elif request.POST.get("update_user"):
            data = json.loads(request.POST.get("update_user"))
            data.update(
                {"first_name": self.remove_excess_whitespace(data["first_name"])}
            )
            data.update({"last_name": self.remove_excess_whitespace(data["last_name"])})
            data.update({"address": self.remove_excess_whitespace(data["address"])})
            errors = self.validate_user(data)
            if not errors:
                user = self.model.objects.get(id=data["id"])
                user.document_number = data["document_number"]
                user.first_name = data["first_name"]
                user.last_name = data["last_name"]
                user.email = data["email"]
                user.address = data["address"]
                user.phone = data["phone"]
                user.save()
                server_response = {
                    "response": True,
                    "redirect": "/library/user/",
                    "status": 200,
                }
            else:
                server_response = {
                    "response": False,
                    "detail": errors,
                    "status": 400,
                }
        else:
            server_response = {
                "response": False,
                "detail": "Bad Request",
                "status": 400,
            }
        return HttpResponse(json.dumps(server_response))

    def password_generator(self, **kwargs):
        upper_case = tuple("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        lower_case = tuple([char.lower() for char in upper_case])
        symbols = ("!", "#", "$", "%", "&", "/", "=", ")", "(", "*", "+", "-", ".")
        numbers = ("1", "2", "3", "4", "5", "6", "7", "8", "9", "0")
        characters = (
            kwargs.get("characters")
            if not kwargs.get("characters") is None
            else upper_case + lower_case + numbers + symbols
        )
        length = kwargs.get("length") if not kwargs.get("length") is None else 5
        password = tuple([random.choice(characters) for index in range(length)])
        return "".join(password)
