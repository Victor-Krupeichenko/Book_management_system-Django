from django.urls import path
from api.v1.views import (
    ListLanguage, CreateLanguage, DeleteLanguage, UpdateLanguage, ListGenre, CreateGenre, DeleteGenre, UpdateGenre,
    ListPublisher, CreatePublisher, DeletePublisher, PUTUpdatePublisher, PATCHUpdatePublisher
)

urlpatterns = [
    path("list-languages/", ListLanguage.as_view()),
    path("add-language/", CreateLanguage.as_view()),
    path("delete-language/<int:pk>/", DeleteLanguage.as_view()),
    path("update-language/<int:pk>/", UpdateLanguage.as_view()),
    path("list-genres/", ListGenre.as_view()),
    path("add-genre/", CreateGenre.as_view()),
    path("delete-genre/<int:pk>/", DeleteGenre.as_view()),
    path("update-genre/<int:pk>/", UpdateGenre.as_view()),
    path("list-publisher/", ListPublisher.as_view()),
    path("add-publisher/", CreatePublisher.as_view()),
    path("delete-publisher/<int:pk>/", DeletePublisher.as_view()),
    path("put-update-publisher/<int:pk>/", PUTUpdatePublisher.as_view()),
    path("patch-update-publisher/<int:pk>/", PATCHUpdatePublisher.as_view()),
]
