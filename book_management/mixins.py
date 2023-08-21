from django.contrib import messages
from django.shortcuts import redirect


class MixinCreateView:
    """Миксин для валидации форм и отправки сообщений"""
    field_name = None
    error_message = "Форма заполнена некорректно"

    def __init__(self):
        self.request = None

    def form_valid(self, form, success_message):
        """Если форма валидна будет показ сообщения"""
        try:
            form.save()
            field = form.cleaned_data.get(self.field_name)
            messages.success(self.request, success_message.format(field=field))
            return redirect("home")
        except Exception as ex:
            messages.error(self.request, f"{ex}")
        return super().form_valid(form)

    def form_invalid(self, form):
        """Если форма не валидна будет показ сообщения"""
        messages.error(self.request, self.error_message)
        return super().form_invalid(form)
