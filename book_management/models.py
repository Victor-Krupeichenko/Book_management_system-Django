import os
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from autoslug import AutoSlugField
from uuslug import uuslug


def instance_title(instance):
    """Возвращает название для формирования slug"""
    return instance.title


def slugify_value(value):
    """Возвращает новую строку названия в которой все пробелы заменены на -(тире)"""
    return value.replace(" ", "-")


def path_cover_for_book(instance, filename):
    """Сохраняет обложку для книги в папку с названием книги"""
    return os.path.join(instance.title, filename)


class BaseModelWithSlug(models.Model):
    """
    Базовая модель от которой наследуются остальные модели
    Эта базовая модель добавляет поля slug
    """
    slug = AutoSlugField(
        max_length=250, unique=True, db_index=True, populate_from=instance_title,
        slugify=slugify_value
    )

    class Meta:
        """Указывает что это класс абстрактный и для него не будет создана таблица в базе данных"""
        abstract = True


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

    def __str__(self):
        """Преобразует объект в строку"""
        return self.title

    def save(self, *args, **kwargs):
        """Сохраняет slug вместо кириллицы -> латиницей"""
        self.slug = uuslug(self.title, instance=self)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ["title"]
        verbose_name = "Книга"
        verbose_name_plural = "Книги"


class Author(BaseModelWithSlug):
    """Модель таблицы для автора книги"""
    first_name = models.CharField(max_length=70, verbose_name="Имя автора")
    last_name = models.CharField(max_length=100, verbose_name="Фамилия автора")
    country = models.CharField(max_length=168, blank=True, verbose_name="Страна")

    def __str__(self):
        """Преобразует объект в строку"""
        return self.first_name

    def save(self, *args, **kwargs):
        """Сохраняет slug вместо кириллицы -> латиницей"""
        self.slug = uuslug(self.first_name, instance=self)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Автор"
        verbose_name_plural = "Авторы"


class Publisher(BaseModelWithSlug):
    """Модель таблицы для издательства книги"""
    title = models.CharField(max_length=100, unique=True, verbose_name="Названия издательства")
    address = models.CharField(max_length=250, verbose_name="Адрес издательства")
    email_address = models.EmailField(max_length=250, unique=True, blank=True, verbose_name="Email адрес")

    def __str__(self):
        """Преобразует объект в строку"""
        return self.title

    def save(self, *args, **kwargs):
        """Сохраняет slug вместо кириллицы -> латиницей"""
        self.slug = uuslug(self.title, instance=self)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Издательство"
        verbose_name_plural = "Издательства"


class Genre(BaseModelWithSlug):
    """Модель таблицы для жанра книги"""
    title = models.CharField(max_length=50, unique=True, verbose_name="Жанр")

    def __str__(self):
        """Преобразует объект в строку"""
        return self.title

    def save(self, *args, **kwargs):
        """Сохраняет slug вместо кириллицы -> латиницей"""
        self.slug = uuslug(self.title, instance=self)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"


class Language(BaseModelWithSlug):
    """Модель таблицы для языка книги"""
    title = models.CharField(max_length=30, unique=True, verbose_name="Язык книги")

    def __str__(self):
        """Преобразует объект в строку"""
        return self.title

    def save(self, *args, **kwargs):
        """Сохраняет slug вместо кириллицы -> латиницей"""
        self.slug = uuslug(self.title, instance=self)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Язык книги"
        verbose_name_plural = "Языки"
