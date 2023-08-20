from django.urls import path
from .views import CreateBook, AllBookView

urlpatterns = [
    path('', AllBookView.as_view(), name="home"),
    path('add-book/', CreateBook.as_view(), name="add_book"),
]
