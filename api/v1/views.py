from rest_framework.response import Response
from rest_framework.generics import ListAPIView, CreateAPIView, DestroyAPIView, UpdateAPIView
from rest_framework import status
from api.v1.serializers import LanguageSerializer, GenreSerializer, PublisherSerializer
from book_management.models import Language, Genre, Publisher
from django.http import Http404
from .utils import BasePublisherUpdate


class ListLanguage(ListAPIView):
    """Показ всех языков"""

    queryset = Language.objects.all()
    serializer_class = LanguageSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class CreateLanguage(CreateAPIView):
    """Добавить язык"""

    serializer_class = LanguageSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)  # Сохранение объекта
            response = {
                "message": f"Язык {serializer.validated_data.get('title')} добавлен"
            }
            return Response(data=response, status=status.HTTP_201_CREATED)
        else:
            response = {
                "error": serializer.errors
            }
            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)


class DeleteLanguage(DestroyAPIView):
    """Удаления языка"""
    serializer_class = LanguageSerializer
    queryset = Language.objects.all()

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()  # Получение конкретного объекта для удаления
            self.perform_destroy(instance)  # Удаление объекта
            response = {
                "message": f"Язык {instance} удален."
            }
            return Response(data=response, status=status.HTTP_204_NO_CONTENT)
        except Http404:
            response = {
                "error": "Ни один язык не соответствует заданному запросу."
            }
            return Response(data=response, status=status.HTTP_404_NOT_FOUND)


class UpdateLanguage(UpdateAPIView):
    """Обновление языка"""
    serializer_class = LanguageSerializer
    queryset = Language.objects.all()

    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, request.data)
            old_title = instance.title  # Храним старое значение
            if serializer.is_valid():
                self.perform_update(serializer)  # Сохраняем обновленный объект
                response = {
                    "message": f"Язык {old_title} обновлен на {instance.title}"
                }
                return Response(data=response, status=status.HTTP_200_OK)
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Http404:
            response = {
                "error": "Ни один язык не соответствует заданному запросу."
            }
            return Response(data=response, status=status.HTTP_404_NOT_FOUND)


class ListGenre(ListAPIView):
    """Показ всех жанров"""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class CreateGenre(CreateAPIView):
    """Создание жанра"""
    serializer_class = GenreSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            response = {
                "message": f"Жанр {serializer.data.get('title')} добавлен"
            }
            return Response(data=response, status=status.HTTP_201_CREATED)
        else:
            response = {
                "error": serializer.errors
            }
            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)


class DeleteGenre(DestroyAPIView):
    """Удаление жанра"""
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            response = {
                "message": f"Жанр {instance.title} удален."
            }
            return Response(data=response, status=status.HTTP_204_NO_CONTENT)
        except Http404:
            response = {
                "error": "Ни один из жанров не соответствует запросу."
            }
            return Response(data=response, status=status.HTTP_404_NOT_FOUND)


class UpdateGenre(UpdateAPIView):
    """Обновление жанра"""
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()

    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, request.data)
            old_genre = instance.title
            if serializer.is_valid():
                self.perform_update(serializer)
                response = {
                    "message": f"Жанр {old_genre} обновлен на {instance.title}"
                }
                return Response(data=response, status=status.HTTP_200_OK)
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Http404:
            response = {
                "error": "Ни один из жанров не соответствует запросу."
            }
            return Response(data=response, status=status.HTTP_404_NOT_FOUND)


class ListPublisher(ListAPIView):
    """Показ всех издателей"""
    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class CreatePublisher(CreateAPIView):
    """Добавление издателя"""
    serializer_class = PublisherSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            publisher = {
                "title": serializer.data.get("title"),
                "address": serializer.data.get("address"),
                "email_address": serializer.data.get("email_address")
            }
            response = {
                "message": f"Издатель: {publisher} создан."
            }
            return Response(data=response, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeletePublisher(DestroyAPIView):
    """Удаление издателя"""

    def get_queryset(self):
        return Publisher.objects.filter(pk=self.kwargs["pk"])

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            response = {
                "message": f"Издатель {instance.title} удален."
            }
            return Response(data=response, status=status.HTTP_204_NO_CONTENT)
        except Http404:
            response = {
                "error": "Ни один из издателей не соответствует запросу."
            }
            return Response(data=response, status=status.HTTP_404_NOT_FOUND)


class PUTUpdatePublisher(BasePublisherUpdate):
    """Полное обновление издателя"""

    serializer_class = PublisherSerializer
    model = Publisher
    partial = False  # Необходимо указать все поля при обновлении


class PATCHUpdatePublisher(BasePublisherUpdate):
    """Частичное обновление издателя"""

    serializer_class = PublisherSerializer
    model = Publisher
    partial = True  # Необходимо указать только те поля которые нужно обновить
