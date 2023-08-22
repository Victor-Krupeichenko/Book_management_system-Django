from rest_framework.response import Response
from rest_framework.generics import ListAPIView, CreateAPIView, DestroyAPIView, UpdateAPIView
from rest_framework import status
from api.v1.serializers import LanguageSerializer
from book_management.models import Language
from django.http import Http404


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


