from django.shortcuts import redirect
from .forms import FormBook
from django.views.generic import CreateView, ListView, DetailView
from django.contrib import messages
from .models import Book


class CreateBook(CreateView):
    """Контроллер для добавления книги"""
    form_class = FormBook
    template_name = "book_management/form.html"

    def form_valid(self, form):
        """Если форма валидна будет показ сообщения"""
        try:
            form.save()
            messages.success(self.request, f"книга {self.form_class.title} добавлена")
            return redirect("/")
        except Exception as ex:
            messages.error(self.request, f"{ex}")
        return super().form_valid(form)

    def form_invalid(self, form):
        """Если форма не валидна будет показ сообщения"""
        messages.error(self.request, "Форма заполнена не корректно")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        """Добавим в контекст флаг, что сейчас используется именно эта форма"""
        context = super().get_context_data(**kwargs)
        context["add_book_form"] = True
        context["title"] = "ADD BOOK"
        return context


class AllBookView(ListView):
    """Показ всех книг"""
    model = Book
    template_name = "book_management/index.html"
    paginate_by = 10

    def get_queryset(self):
        """Показывает только те книги которые разрешены к показу"""
        return Book.objects.filter(show_book=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "ALL BOOK"
        return context


class DetailBookView(DetailView):
    """Детальный просмотр книги"""
    model = Book
    template_name = "book_management/book_detail.html"
