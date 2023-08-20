from django.urls import path
from .views import CreateBook, AllBookView, DetailBookView, UpdateBook

urlpatterns = [
    path('', AllBookView.as_view(), name="home"),
    path('add-book/', CreateBook.as_view(), name="add_book"),
    path("detail-book-view/<str:slug>/", DetailBookView.as_view(), name="detail_book"),
    path("update-info-for-book/<str:slug>/", UpdateBook.as_view(), name="update_book"),
]
