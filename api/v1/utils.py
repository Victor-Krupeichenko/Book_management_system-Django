from django.http import Http404
from rest_framework import status
from rest_framework.generics import UpdateAPIView
from rest_framework.response import Response


def old_data_publisher(instance):
    """
    Принимает объект модели,
    возвращает старые атрибутов объекта
    """
    old_data = {
        "old_title": instance.title,
        "old_address": instance.address,
        "old_email_address": instance.email_address
    }
    return old_data


def new_data_publisher(instance):
    """
    Принимает объект модели,
    возвращает новые атрибутов объекта
    """
    new_data = {
        "new_title": instance.title,
        "new_address": instance.address,
        "new_email_address": instance.email_address
    }
    return new_data


class BasePublisherUpdate(UpdateAPIView):
    """Базовый класс для полного и частичного обновления издательства"""
    serializer_class = None
    model = None
    partial = False  # partial=True - указывает на частичное обновление.

    def get_queryset(self):
        return self.model.objects.filter(pk=self.kwargs["pk"])

    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, request.data, partial=self.partial)  # partial=True-частичное обн
            old_data = old_data_publisher(instance)
            if serializer.is_valid():
                self.perform_update(serializer)
                new_data = new_data_publisher(instance)
                response = {
                    "message": f"Издатель: {old_data} обновлен на {new_data}"
                }
                return Response(data=response, status=status.HTTP_200_OK)
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Http404:
            response = {
                "error": "Ни одно из издательств не соответствует запросу."
            }
            return Response(data=response, status=status.HTTP_404_NOT_FOUND)
