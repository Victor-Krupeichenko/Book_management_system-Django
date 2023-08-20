from django.urls import path
from .views import CreateBook, AllBookView, DetailBookView

urlpatterns = [
    path('', AllBookView.as_view(), name="home"),
    path('add-book/', CreateBook.as_view(), name="add_book"),
    path("detail-book-view/<str:slug>/", DetailBookView.as_view(), name="detail_book"),
]
