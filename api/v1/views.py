from api.v1.serializers import LanguageSerializer, GenreSerializer, PublisherSerializer, AuthorSerializer
from book_management.models import Language, Genre, Publisher, Author
from .utils import (
    BaseUpdate, BaseListView, BaseCreateView, BaseDeleteView, data_publisher, data_author, data_language_or_genre,
    data_author_create, data_publisher_create
)


class ListLanguage(BaseListView):
    """Показ всех языков"""

    model = Language
    serializer_class = LanguageSerializer


class CreateLanguage(BaseCreateView):
    """Добавить язык"""

    serializer_class = LanguageSerializer
    response = {
        "message": f"Язык добавлен"
    }


class DeleteLanguage(BaseDeleteView):
    """Удаления языка"""

    model = Language


class UpdateLanguage(BaseUpdate):
    """Обновление языка"""

    model = Language
    serializer_class = LanguageSerializer
    data_func = data_language_or_genre


class ListGenre(BaseListView):
    """Показ всех жанров"""

    model = Genre
    serializer_class = GenreSerializer


class CreateGenre(BaseCreateView):
    """Создание жанра"""

    serializer_class = GenreSerializer
    response = {
        "message": "Жанр добавлен"
    }


class DeleteGenre(BaseDeleteView):
    """Удаление жанра"""

    model = Genre


class UpdateGenre(BaseUpdate):
    """Обновление жанра"""

    model = Genre
    serializer_class = GenreSerializer
    data_func = data_language_or_genre


class ListPublisher(BaseListView):
    """Показ всех издателей"""

    model = Publisher
    serializer_class = PublisherSerializer


class CreatePublisher(BaseCreateView):
    """Добавление издателя"""

    serializer_class = PublisherSerializer
    data_func = data_publisher_create


class DeletePublisher(BaseDeleteView):
    """Удаление издателя"""

    model = Publisher


class PUTUpdatePublisher(BaseUpdate):
    """Полное обновление издателя"""

    serializer_class = PublisherSerializer
    model = Publisher
    partial = False  # Необходимо указать все поля при обновлении
    data_func = data_publisher


class PATCHUpdatePublisher(BaseUpdate):
    """Частичное обновление издателя"""

    serializer_class = PublisherSerializer
    model = Publisher
    partial = True  # Необходимо указать только те поля которые нужно обновить
    data_func = data_publisher


class ListAuthor(BaseListView):
    """Показать всех авторов"""

    model = Author
    serializer_class = AuthorSerializer


class CreateAuthor(BaseCreateView):
    """Создание(добавления) автора"""

    serializer_class = AuthorSerializer
    data_func = data_author_create


class DeleteAuthor(BaseDeleteView):
    """Удаления автора"""

    model = Author


class PutUpdateAuthor(BaseUpdate):
    """Полное обновление автора"""

    serializer_class = AuthorSerializer
    model = Author
    data_func = data_author


class PatchUpdateAuthor(BaseUpdate):
    """Частичное обновление автора"""

    serializer_class = AuthorSerializer
    model = Author
    data_func = data_author
    partial = True
