from django.urls import path
from apps.library.views import (
    AdminRequest,
    CategoryRequest,
    BookRequest,
    BookLoanRequest,
    DebtRequest,
    UserRequest,
)


app_name = "library"

urlpatterns = [
    path("admin/", AdminRequest.as_view(), name="admin"),
    path("category/", CategoryRequest.as_view(), name="category"),
    path("book/", BookRequest.as_view(), name="book"),
    path("bookloan/", BookLoanRequest.as_view(), name="bookloan"),
    path("debt/", DebtRequest.as_view(), name="debt"),
    path("user/", UserRequest.as_view(), name="user"),
]
