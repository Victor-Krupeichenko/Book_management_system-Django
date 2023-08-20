from django.urls import path
from .views import CreateBook

urlpatterns = [
    path('add-book/', CreateBook.as_view(), name="add_book"),
]
