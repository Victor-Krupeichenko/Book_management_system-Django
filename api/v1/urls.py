from django.urls import path
from api.v1.views import (
    ListLanguage, CreateLanguage, DeleteLanguage, UpdateLanguage
)

urlpatterns = [
    path("list-languages/", ListLanguage.as_view()),
    path("add-language/", CreateLanguage.as_view()),
    path("delete-language/<int:pk>/", DeleteLanguage.as_view()),
    path("update-language/<int:pk>/", UpdateLanguage.as_view()),
]
