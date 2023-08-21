from django.shortcuts import redirect
from .forms import FormBook, FormPublisher, FormAuthor, FormLanguage, FormGenre
from django.views.generic import CreateView, ListView, DetailView
from django.contrib import messages
from .models import Book, Author, Publisher, Language, Genre
from django.views.generic.edit import UpdateView, DeleteView
from django.urls import reverse_lazy
from .mixins import MixinCreateView


class CreateBook(MixinCreateView, CreateView):
    """Контроллер для добавления книги"""
    form_class = FormBook
    template_name = "book_management/form.html"
    success_message = "Книга {field} добавлена"

    def form_valid(self, form, **kwargs):
        return super().form_valid(form, success_message=self.success_message)

    def form_invalid(self, form):
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


class UpdateBook(MixinCreateView, UpdateView):
    """Обновление информации о книге"""
    model = Book
    template_name = "book_management/form.html"
    form_class = FormBook
    success_message = "Книга {field} обновлена"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["info"] = "Изменить информацию о книге"
        context["update_info"] = True
        return context

    def form_valid(self, form, **kwargs):
        return super().form_valid(form, success_message=self.success_message)


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
        context["author"] = True
        return context


class AllAuthrBook(ListView):
    """Получение списка книг только конкретного автора"""
    model = Book
    template_name = "book_management/index.html"
    paginate_by = 10

    def get_queryset(self):
        return Book.objects.filter(author__slug=self.kwargs["slug"], show_book=True).all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Все книги автора"
        return context


class CreateAuthor(MixinCreateView, CreateView):
    """Добавление автора"""
    form_class = FormAuthor
    template_name = "book_management/form.html"
    field_name = "first_name"
    success_message = "Автор {field} добавлен"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["create_author"] = True
        context["title"] = "Добавить автора"
        return context

    def form_valid(self, form, **kwargs):
        return super().form_valid(form, success_message=self.success_message)

    def form_invalid(self, form):
        return super().form_invalid(form)


class CreatePublisher(MixinCreateView, CreateView):
    """Добавляет издательство"""
    form_class = FormPublisher
    template_name = "book_management/form.html"
    success_message = "Издатель {field} добавлен"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["create_publisher"] = True
        context["title"] = "Добавить издателя"
        return context

    def form_valid(self, form, **kwargs):
        return super().form_valid(form, success_message=self.success_message)

    def form_invalid(self, form):
        return super().form_invalid(form)


class AllPublisherView(ListView):
    """Показать список издательств"""
    model = Publisher
    template_name = "book_management/list_objects.html"

    def get_queryset(self):
        return Publisher.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Список издательств"
        context["publisher"] = True
        return context


class AllPublisherBook(ListView):
    """Показать все книги издательства"""
    model = Book
    template_name = "book_management/index.html"
    paginate_by = 10

    def get_queryset(self):
        return Book.objects.filter(publisher__slug=self.kwargs["slug"]).all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Все книги издательства"
        return context


class DeletePublisher(DeleteView):
    """Удаления издательства"""
    model = Publisher
    template_name = "book_management/list_objects.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        """Тут этот метод исключительно для показа сообщения"""
        instance = self.get_object()
        messages.success(self.request, f"издательство {instance.title} удалено")
        return super().form_valid(form)


class UpdatePublisher(MixinCreateView, UpdateView):
    form_class = FormPublisher
    model = Publisher
    template_name = "book_management/form.html"
    success_message = "Издательство {field} обновлено"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["update_publisher"] = True
        context["title"] = "Обновить издателя"
        return context

    def form_valid(self, form, **kwargs):
        return super().form_valid(form, success_message=self.success_message)


class CreateLanguage(MixinCreateView, CreateView):
    """Добавляет язык на котором написана книга"""
    form_class = FormLanguage
    template_name = "book_management/form.html"
    success_message = "Язык {field} добавлен"

    def form_valid(self, form, **kwargs):
        return super().form_valid(form, success_message=self.success_message)

    def form_invalid(self, form):
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["create_language"] = True
        context["title"] = "Добавить язык"
        return context


class AllLanguageView(ListView):
    """Показ списка языков"""
    model = Language
    template_name = "book_management/list_objects.html"
    paginate_by = 10

    def get_queryset(self):
        return Language.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["language"] = True
        context["title"] = "Все языки"
        return context
