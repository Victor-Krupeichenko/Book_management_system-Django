from django.shortcuts import redirect
from .forms import FormBook
from django.views.generic import CreateView, ListView, DetailView
from django.contrib import messages
from .models import Book, Author, Publisher, Language
from django.views.generic.edit import UpdateView, DeleteView
from django.urls import reverse_lazy


class CreateBook(CreateView):
    """Контроллер для добавления книги"""
    form_class = FormBook
    template_name = "book_management/form.html"

    def form_valid(self, form):
        """Если форма валидна будет показ сообщения"""
        try:
            book = form.save()
            messages.success(self.request, f"книга {book.title} добавлена")
            return redirect("home")
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


class UpdateBook(UpdateView):
    """Обновление информации о книге"""
    model = Book
    template_name = "book_management/form.html"
    form_class = FormBook
    success_url = reverse_lazy("home")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["info"] = "Изменить информацию о книге"
        context["update_info"] = True
        return context

    def form_valid(self, form):
        """Если форма валидна будет показ сообщения"""
        try:
            book = form.save()
            messages.success(self.request, f"книга {book.title} обновлена")
            return redirect("home")
        except Exception as ex:
            messages.error(self.request, f"{ex}")
        return super().form_valid(form)


class DeleteBook(DeleteView):
    """Удаление книги"""
    model = Book
    template_name = "book_management/index.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        """Основная задача этого метода - это показ сообщения после удаления книги"""
        instance = self.get_object()
        book_title = instance.title
        messages.success(self.request, f"книга {book_title} удалена")
        return super().form_valid(form)


class AllAuthorView(ListView):
    """Показ списка всех авторов"""
    model = Author
    template_name = "book_management/list_objects.html"
    paginate_by = 10

    def get_queryset(self):
        return Author.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Список авторов"
        return context


class AllAuthrBook(ListView):
    """Получение списка книг только конкретного автора"""
    model = Book
    template_name = "book_management/index.html"
    paginate_by = 10

    def get_queryset(self):
        return Book.objects.filter(author__slug=self.kwargs["slug"], show_book=True).all()
