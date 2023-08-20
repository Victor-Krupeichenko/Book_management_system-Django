from django import forms

from .models import Book


class FormBook(forms.ModelForm):
    """Форма для добавления книги"""

    class Meta:
        model = Book
        fields = ["title", "author", "publisher", "language", "pages", "cover", "year"]

    def __init__(self, *args, **kwargs):
        """Переопределение метода и добавление виджетов в форму"""
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs["class"] = "form-control"
            self.fields[field].widget.attrs["placeholder"] = self.fields[field].label
            self.fields[field].label = ""
        self.fields["publisher"].empty_label = "Выбери издателя"
