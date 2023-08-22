from django.urls import path
from api.v1.views import (
    ListLanguage, CreateLanguage, DeleteLanguage, UpdateLanguage, ListGenre, CreateGenre, DeleteGenre, UpdateGenre
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
]
