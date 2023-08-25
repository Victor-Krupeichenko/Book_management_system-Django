from django.http import Http404
from rest_framework import status
from rest_framework.generics import (
    UpdateAPIView, ListAPIView, CreateAPIView, DestroyAPIView, RetrieveAPIView, get_object_or_404
)
from rest_framework.response import Response


def data_publisher(*args, instance):
    """
    Принимает объект модели Publisher,
    возвращает атрибуты этого объекта
    """

    data = {
        "title": instance.title,
        "address": instance.address,
        "email_address": instance.email_address,

    }
    return data


def data_author(*args, instance):
    """
    Принимает объект модели Author,
    возвращает атрибуты этого объекта
    """

    data = {
        "first_name": instance.first_name,
        "last_name": instance.last_name,
        "country": instance.country
    }
    return data


def data_language_or_genre(*args, instance):
    """
    Принимает объект модели Language или Author,
    возвращает атрибуты этого объекта
    """

    data = {
        "title": instance.title
    }
    return data


def data_author_create(*args, serializer):
    """Возвращает подробное описание созданного объекта модели Author"""

    data = {
        "first_name": serializer.data.get("first_name"),
        "last_name": serializer.data.get("last_name"),
        "country": serializer.data.get("country")
    }
    response = {
        "message": f"Автор {data} создан."
    }
    return response


def data_publisher_create(*args, serializer):
    """Возвращает подробное описание созданного объекта модели Publisher"""

    publisher = {
        "title": serializer.data.get("title"),
        "address": serializer.data.get("address"),
        "email_address": serializer.data.get("email_address")
    }
    response = {
        "message": f"Издатель: {publisher} создан."
    }
    return response


class BaseUpdate(UpdateAPIView):
    """
    Базовый класс для полного и частичного обновления
    serializer_class - Класс сериализатор
    model - Модель экземпляр которой будем обновлять
    partial=True - указывает на частичное обновление объекта(по умолчанию False)
    data_func - Функция, которая будет возвращать старые значение и обновленные значения
    !!! Функцию нужно писать отдельно
    (если data_func не указана будет возвращено значение по умолчанию)
    """

    serializer_class = None
    model = None
    partial = False
    data_func = None

    def get_queryset(self):
        """Возвращает конкретный объект из базы данных"""

        return self.model.objects.filter(pk=self.kwargs["pk"])

    def update(self, request, *args, **kwargs):
        """Обновляет сам объект"""
        old_data = None
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, request.data, partial=self.partial)  # partial=True-частичное обн
            if self.data_func:
                old_data = self.data_func(instance=instance)  # Получаем и сохраняем старое значение
            if serializer.is_valid():
                self.perform_update(serializer)
                if self.data_func:
                    new_data = self.data_func(instance=instance)  # Получаем и сохраняем новое значение
                    response = {
                        "message": f"{self.model.__name__}: old_: {old_data} обновлен на new_: {new_data}"
                    }
                else:
                    response = {
                        "message": f"Объект {self.model.__name__} обновлен"
                    }
                return Response(data=response, status=status.HTTP_200_OK)
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Http404:
            response = {
                "error": f"Ни один из объектов {self.model.__name__} не соответствует запросу."
            }
            return Response(data=response, status=status.HTTP_404_NOT_FOUND)


class BaseListView(ListAPIView):
    """
    Базовый класс вывода всех объектов
    serializer_class - Сериализатор модели
    model = Модель у которой необходимо получить все объекты
    """

    serializer_class = None
    model = None

    def get_queryset(self):
        """Получение всех объектов"""

        return self.model.objects.all()

    def list(self, request, *args, **kwargs):
        """Показ всех объектов"""

        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class BaseCreateView(CreateAPIView):
    """
    Базовый класс создания объекта
    serializer_class - Класс сериализатор
    response - после создания объекта
    data_func - Функция, которая будет возвращать подробное описание созданного объекта
    !!! Функцию нужно писать отдельно
    !!! Может быть указан либо response, либо data_func
    (если указаны оба параметра то работать будет только response)
    (если не указаны не response и не data_func - то будет использован ответ по умолчанию)
    """

    serializer_class = None
    response = None
    data_func = None

    def create(self, request, *args, **kwargs):
        """Создание объекта"""

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)  # создание объекта
            if self.response:
                response = self.response
            elif self.data_func:
                response = self.data_func(serializer=serializer)
            else:
                response = "Объект создан"
            return Response(data=response, status=status.HTTP_201_CREATED)
        else:
            response = {
                "error": serializer.errors
            }
            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)


class BaseDeleteView(DestroyAPIView):
    """
    Базовый класс для удаления
    model - объект какой модели будет удален
    """

    model = None

    def get_queryset(self):
        """Получение конкретного объекта"""

        return self.model.objects.filter(pk=self.kwargs["pk"])

    def destroy(self, request, *args, **kwargs):
        """Удаление объекта"""

        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            response = {
                "message": f"Объект {self.model.__name__}: '{instance}' удален."
            }
            return Response(data=response, status=status.HTTP_204_NO_CONTENT)
        except Http404:
            response = {
                "error": f"Ни один {self.model.__name__.lower()} не соответствует заданному запросу"
            }
            return Response(data=response, status=status.HTTP_404_NOT_FOUND)


class BaseDetailView(RetrieveAPIView):
    """Показ конкретного объекта"""

    serializer_class = None
    model = None

    def get_object(self):
        return get_object_or_404(self.model, pk=self.kwargs["pk"])
