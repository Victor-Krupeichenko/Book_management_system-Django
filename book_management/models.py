from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from .utils import BaseModelWithSlug, path_cover_for_book
from django.urls import reverse_lazy


class Book(BaseModelWithSlug):
    """Модель таблицы для книги"""
    title = models.CharField(max_length=200, verbose_name="Название книги")
    author = models.ManyToManyField('Author', related_name="author", db_index=True, verbose_name="Авторы")
    publisher = models.ForeignKey(
        "Publisher", on_delete=models.CASCADE, related_name="publisher", verbose_name="Издательство"
    )
    genre = models.ManyToManyField("Genre", related_name="genre", verbose_name="Жанр")
    language = models.ManyToManyField("Language", related_name="language", verbose_name="Язык книги")
    pages = models.IntegerField(default=0, verbose_name="Страницы")
    cover = models.ImageField(upload_to=path_cover_for_book, verbose_name="Обложка", blank=True, null=True)
    year = models.IntegerField(
        verbose_name="Год издания",
        validators=[
            MinValueValidator(1000), MaxValueValidator(3000)
        ]
    )
    show_book = models.BooleanField(default=True, verbose_name="Показать книгу")

    class Meta:
        """
        Русские название разделов
        в единственном и множественном числе
        """
        verbose_name = "Книга"
        verbose_name_plural = "Книги"

    def get_absolute_url(self):
        """Согласно конвенции абсолютный путь к конкретной книге"""
        context = {
            "slug": self.slug
        }
        return reverse_lazy("detail_book", kwargs=context)


class Author(BaseModelWithSlug):
    """Модель таблицы для автора книги"""
    first_name = models.CharField(max_length=70, verbose_name="Имя автора")
    last_name = models.CharField(max_length=100, verbose_name="Фамилия автора")
    country = models.CharField(max_length=168, blank=True, verbose_name="Страна")

    def save(self, *args, **kwargs):
        self.slug_field = self.first_name
        super().save(*args, **kwargs)

    def __str__(self):
        """Преобразует объект в строку"""
        return f"{self.first_name} {self.last_name}"

    class Meta:
        """
        Русские название разделов
        в единственном и множественном числе
        и сортировка по полю first_name
        """
        verbose_name = "Автор"
        verbose_name_plural = "Авторы"
        ordering = ["first_name"]


class Publisher(BaseModelWithSlug):
    """Модель таблицы для издательства книги"""
    title = models.CharField(max_length=100, unique=True, verbose_name="Названия издательства")
    address = models.CharField(max_length=250, verbose_name="Адрес издательства")
    email_address = models.EmailField(max_length=250, unique=True, blank=True, verbose_name="Email адрес")

    class Meta:
        """
        Русские название разделов
        в единственном и множественном числе
        """
        verbose_name = "Издательство"
        verbose_name_plural = "Издательства"


class Genre(BaseModelWithSlug):
    """Модель таблицы для жанра книги"""
    title = models.CharField(max_length=50, unique=True, verbose_name="Жанр")

    class Meta:
        """
        Русские название разделов
        в единственном и множественном числе
        """
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"


class Language(BaseModelWithSlug):
    """Модель таблицы для языка книги"""
    title = models.CharField(max_length=30, unique=True, verbose_name="Язык книги")

    class Meta:
        """
        Русские название разделов
        в единственном и множественном числе
        """
        verbose_name = "Язык книги"
        verbose_name_plural = "Языки книги"
