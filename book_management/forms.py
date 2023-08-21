from django import forms

from .models import Book, Publisher, Author, Language, Genre


class BaseFieldForm(forms.ModelForm):
    """Добавляет виджеты для полей формы"""

    def __init__(self, *args, **kwargs):
        """Переопределение метода и добавление виджетов в форму"""
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs["class"] = "form-control"
            self.fields[field].widget.attrs["placeholder"] = self.fields[field].label
            self.fields[field].label = ""


class FormBook(BaseFieldForm):
    """Форма для добавления книги"""

    class Meta:
        model = Book
        fields = ["title", "author", "publisher", "language", "pages", "cover", "year"]

    def __init__(self, *args, **kwargs):
        """Переопределение метода и добавление виджетов в форму"""
        super().__init__(*args, **kwargs)
        self.fields["publisher"].empty_label = "Выбери издателя"


class FormPublisher(BaseFieldForm):
    """Форма для модели Publisher"""

    class Meta:
        model = Publisher
        fields = ["title", "address", "email_address"]
