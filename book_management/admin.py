from django.contrib import admin
from .models import *


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """Регистрация в админке модели Book"""

    list_display = ["title", "display_authors", "publisher", "year", "cover", "pages", "show_book"]

    def display_authors(self, obj):
        """Показывает список автора(список авторов) из связанного с книгой полем (ManyToManyField)"""
        authors = ', '.join(f"{aut.first_name} {aut.last_name}" for aut in obj.author.all())
        return authors

    display_authors.short_description = "авторы"

    list_editable = ["show_book"]
    list_filter = ["year", "show_book"]
    search_fields = ["title", "author__first_name", "author__last_name"]
    ordering = ["title", "year"]
