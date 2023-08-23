from rest_framework import serializers
from book_management.models import Book, Author, Publisher, Genre, Language


class LanguageSerializer(serializers.ModelSerializer):
    """Сериализует модель Language"""

    class Meta:
        model = Language
        fields = ["id", "title"]


class GenreSerializer(serializers.ModelSerializer):
    """Сериализует модель Genre"""

    class Meta:
        model = Genre
        fields = ["id", "title"]


class PublisherSerializer(serializers.ModelSerializer):
    """Суриализует модель Publisher"""

    class Meta:
        model = Publisher
        fields = ["id", "title", "address", "email_address"]


class AuthorSerializer(serializers.ModelSerializer):
    """Сериализует модель Author"""

    class Meta:
        model = Author
        fields = ["id", "first_name", "last_name", "country"]


class AllBookSerializer(serializers.ModelSerializer):
    """Сериализует модель Book для показа книг"""

    author = AuthorSerializer(many=True)  # many=True - указывает что поля представляет множество объектов
    publisher = PublisherSerializer()
    genre = GenreSerializer(many=True)
    language = LanguageSerializer(many=True)

    class Meta:
        model = Book
        fields = ["id", "title", "language", "author", "publisher", "genre", "pages", "cover", "year"]


class BookSerializer(serializers.ModelSerializer):
    """Сериализатор модели Book для создания(добавления) и обновления книги"""
    class Meta:
        model = Book
        fields = ["title", "language", "author", "publisher", "genre", "pages", "cover", "year"]
