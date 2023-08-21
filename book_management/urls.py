from django.urls import path
from .views import CreateBook, AllBookView, DetailBookView, UpdateBook, DeleteBook, AllAuthorView, AllAuthrBook

urlpatterns = [
    path("", AllBookView.as_view(), name="home"),
    path("add-book/", CreateBook.as_view(), name="add_book"),
    path("detail-book-view/<str:slug>/", DetailBookView.as_view(), name="detail_book"),
    path("update-info-for-book/<str:slug>/", UpdateBook.as_view(), name="update_book"),
    path("delete-book/<str:slug>/", DeleteBook.as_view(), name="delete_book"),
    path("all-author/", AllAuthorView.as_view(), name="all_author"),
    path("all-author-book/<str:slug>/", AllAuthrBook.as_view(), name="all_author_book"),
]
