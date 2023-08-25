from django.urls import path
from api.v1.views import (
    ListLanguage, CreateLanguage, DeleteLanguage, UpdateLanguage, ListGenre, CreateGenre, DeleteGenre, UpdateGenre,
    ListPublisher, CreatePublisher, DeletePublisher, PUTUpdatePublisher, PATCHUpdatePublisher, ListAuthor,
    CreateAuthor, DeleteAuthor, PutUpdateAuthor, PatchUpdateAuthor, ListBook, CreateBook, PutUpdateBook,
    PatchUpdateBook, DeleteBook, DetailBookView
)

app_name = "api"
urlpatterns = [
    path("list-languages/", ListLanguage.as_view(), name="list_language"),
    path("add-language/", CreateLanguage.as_view(), name="add_language"),
    path("delete-language/<int:pk>/", DeleteLanguage.as_view(), name="delete_language"),
    path("update-language/<int:pk>/", UpdateLanguage.as_view(), name="update_language"),
    path("list-genres/", ListGenre.as_view(), name="list_genre"),
    path("add-genre/", CreateGenre.as_view(), name="add_genre"),
    path("delete-genre/<int:pk>/", DeleteGenre.as_view(), name="delete_genre"),
    path("update-genre/<int:pk>/", UpdateGenre.as_view(), name="update_genre"),
    path("list-publisher/", ListPublisher.as_view(), name="list_publisher"),
    path("add-publisher/", CreatePublisher.as_view(), name="add_publisher"),
    path("delete-publisher/<int:pk>/", DeletePublisher.as_view(), name="delete_publisher"),
    path("put-update-publisher/<int:pk>/", PUTUpdatePublisher.as_view(), name="put_update_publisher"),
    path("patch-update-publisher/<int:pk>/", PATCHUpdatePublisher.as_view(), name="patch_update_publisher"),
    path("list-author/", ListAuthor.as_view(), name="list_author"),
    path("add-author/", CreateAuthor.as_view(), name="add_author"),
    path("delete-author/<int:pk>/", DeleteAuthor.as_view(), name="delete_author"),
    path("put-update-author/<int:pk>/", PutUpdateAuthor.as_view(), name="put_update_author"),
    path("patch-update-author/<int:pk>/", PatchUpdateAuthor.as_view(), name="patch_update_author"),
    path("list-book/", ListBook.as_view(), name="list_book"),
    path("add-book/", CreateBook.as_view(), name="add_book"),
    path("put-update-book/<int:pk>/", PutUpdateBook.as_view(), name="put_update_book"),
    path("patch-update-book/<int:pk>/", PatchUpdateBook.as_view(), name="patch_update_book"),
    path("delete-book/<int:pk>/", DeleteBook.as_view(), name="delete_book"),
    path("detail-book-view/<int:pk>/", DetailBookView.as_view(), name="detail_book_view"),
]
