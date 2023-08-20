from django.contrib import admin
from .models import *


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """Регистрация в админке модели Book"""

    list_display = ["title", "display_authors", "publisher", "year", "cover", "pages", "show_book"]

    def display_authors(self, obj):
        """Показывает список автора(список авторов) из связанного с книгой полем (ManyToManyField)"""
        authors = ', '.join(f"{aut}" for aut in obj.author.all())
        return authors

    display_authors.short_description = "авторы"
    list_display_links = ["title", "display_authors", "publisher"]
    list_editable = ["show_book"]
    list_filter = ["year", "show_book"]
    search_fields = ["title", "author__first_name", "author__last_name"]
    ordering = ["title", "year"]
    raw_id_fields = ["author", "publisher"]  # Поисковый виджет для этих полей вместо выпадающего списка


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    """Регистрация в админке модели Author"""
    list_display = ["first_name", "last_name", "country"]
    list_display_links = ["first_name", "last_name"]
    search_fields = ["first_name", "last_name"]


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    """Регистрация в админке модели Publisher"""
    list_display = ["title", "address", "email_address"]
    list_display_links = ["title", "address"]
    search_fields = ["title", "address"]


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """Регистрация в админке модели Genre"""
    list_display = ["title"]
    list_display_links = ["title"]
    search_fields = ["title"]


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    """Регистрация в админке модели Language"""
    list_display = ["title"]
    list_display_links = ["title"]
    search_fields = ["title"]
