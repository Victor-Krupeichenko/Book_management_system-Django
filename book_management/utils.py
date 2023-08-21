import os
from django.db import models
from autoslug import AutoSlugField
from uuslug import uuslug


def instance_field(instance):
    """Возвращает поля для формирования slug"""
    if instance.title:
        return instance.title
    return instance.first_name


def slugify_value(value):
    """Возвращает новую строку названия в которой все пробелы заменены на -(тире)"""
    return value.replace(" ", "-")


def path_cover_for_book(instance, filename):
    """Сохраняет обложку для книги в папку с названием книги"""
    return os.path.join(instance.title, filename)


class BaseModelWithSlug(models.Model):
    """
    Базовая модель от которой наследуются остальные модели
    Эта базовая модель добавляет поля slug, сортировку объектов по умолчанию(поля title),
    генерирует slug из указанного поля
    """
    slug = AutoSlugField(
        max_length=250, unique=True, db_index=True, populate_from=instance_field, slugify=slugify_value
    )

    def __str__(self):
        """Преобразует объект в строку"""
        return self.title

    def save(self, *args, **kwargs):
        if hasattr(self, "slug_field"):  # проверяет, имеется ли у объекта атрибут с заданным именем - "slug_field"
            self.slug = uuslug(self.slug_field, instance=self)  # Генерируем slug на основе этого поля
        else:
            self.slug = uuslug(self.title, instance=self)  # Генерируем slug на основе этого поля title
        super().save(*args, **kwargs)

    class Meta:
        abstract = True  # Указывает что это класс абстрактный и для него не будет создана таблица в базе данных
        ordering = ["title"]  # Указываем какая сортировка объектов будет по умолчанию title
