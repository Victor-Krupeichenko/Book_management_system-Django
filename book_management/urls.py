from django.urls import path
from .views import (
    CreateBook, AllBookView, DetailBookView, UpdateBook, DeleteBook, AllAuthorView, AllAuthrBook, CreatePublisher,
    AllPublisherView, AllPublisherBook, CreateAuthor, DeletePublisher, UpdatePublisher, CreateLanguage, AllLanguageView,
    AllLanguageBook, DeleteLanguage, CreateGenre, AllGenreBook, AllGenreView, DeleteGenre
)

urlpatterns = [
    path("", AllBookView.as_view(), name="home"),
    path("add-book/", CreateBook.as_view(), name="add_book"),
    path("detail-book-view/<str:slug>/", DetailBookView.as_view(), name="detail_book"),
    path("update-info-for-book/<str:slug>/", UpdateBook.as_view(), name="update_book"),
    path("delete-book/<str:slug>/", DeleteBook.as_view(), name="delete_book"),
    path("all-author/", AllAuthorView.as_view(), name="all_author"),
    path("all-author-book/<str:slug>/", AllAuthrBook.as_view(), name="all_author_book"),
    path("create_publisher/", CreatePublisher.as_view(), name="create_publisher"),
    path("all-publisher/", AllPublisherView.as_view(), name="all_publisher"),
    path("all-publisher-book/<str:slug>/", AllPublisherBook.as_view(), name="all_publisher_book"),
    path("add-author/", CreateAuthor.as_view(), name="add_author"),
    path("delete-publisher/<str:slug>/", DeletePublisher.as_view(), name="delete_publisher"),
    path("update-publisher/<str:slug>/", UpdatePublisher.as_view(), name="update_publisher"),
    path("create-language/", CreateLanguage.as_view(), name="create_language"),
    path("all-language/", AllLanguageView.as_view(), name="all_language"),
    path("all-book-language/<str:slug>/", AllLanguageBook.as_view(), name="all_language_book"),
    path("delete-language/<str:slug>/", DeleteLanguage.as_view(), name="delete_language"),
    path("add-genre/", CreateGenre.as_view(), name="add_genre"),
    path("all-book-genre/<str:slug>/", AllGenreBook.as_view(), name="all_genre_book"),
    path("all-genre/", AllGenreView.as_view(), name="all_genre"),
    path("delete-genre/<str:slug>/", DeleteGenre.as_view(), name="delete_genre"),
]
