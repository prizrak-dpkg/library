from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from apps.library.models import *


#   ====================   #
#   Table name: Category   #
#   ====================   #
class CategoryResource(resources.ModelResource):
    class Meta:
        model = Category
        import_id_fields = ["id"]


class CategoryAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    search_fields = [
        "name",
    ]
    list_display = (
        "id",
        "registration_date",
        "modification_date",
        "status",
        "name",
        "standar_loan",
        "penalty_payment",
    )
    resource_class = CategoryResource


admin.site.register(
    Category,
    CategoryAdmin,
)


#   ==================   #
#   Table name: Author   #
#   ==================   #
class AuthorResource(resources.ModelResource):
    class Meta:
        model = Author
        import_id_fields = ["id"]


class AuthorAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    search_fields = [
        "last_name",
    ]
    list_display = (
        "id",
        "registration_date",
        "modification_date",
        "status",
        "first_name",
        "last_name",
    )
    resource_class = AuthorResource


admin.site.register(
    Author,
    AuthorAdmin,
)


#   =====================   #
#   Table name: Publisher   #
#   =====================   #
class PublisherResource(resources.ModelResource):
    class Meta:
        model = Publisher
        import_id_fields = ["id"]


class PublisherAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    search_fields = [
        "name",
    ]
    list_display = (
        "id",
        "registration_date",
        "modification_date",
        "status",
        "name",
    )
    resource_class = PublisherResource


admin.site.register(
    Publisher,
    PublisherAdmin,
)


#   ================   #
#   Table name: Book   #
#   ================   #
class BookResource(resources.ModelResource):
    class Meta:
        model = Book
        import_id_fields = ["id"]


class BookAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    search_fields = [
        "title",
    ]
    list_display = (
        "id",
        "registration_date",
        "modification_date",
        "status",
        "title",
        "author",
        "publisher",
        "category",
        "language",
        "number_pages",
        "year_publication",
        "available_units",
    )
    resource_class = BookResource


admin.site.register(
    Book,
    BookAdmin,
)


#   ====================   #
#   Table name: BookLoan   #
#   ====================   #
class BookLoanResource(resources.ModelResource):
    class Meta:
        model = BookLoan
        import_id_fields = ["id"]


class BookLoanAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    search_fields = [
        "user__document_number",
    ]
    list_display = (
        "key",
        "registration_date",
        "modification_date",
        "returned",
        "user",
        "book",
    )
    resource_class = BookLoanResource


admin.site.register(
    BookLoan,
    BookLoanAdmin,
)


#   ================   #
#   Table name: Debt   #
#   ================   #
class DebtResource(resources.ModelResource):
    class Meta:
        model = Debt
        import_id_fields = ["id"]


class DebtAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    search_fields = [
        "book_loan__user__document_number",
    ]
    list_display = (
        "id",
        "book_loan",
        "value_paid",
        "debt_paid_off",
    )
    resource_class = DebtResource


admin.site.register(
    Debt,
    DebtAdmin,
)
