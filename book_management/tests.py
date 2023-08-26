from django.test import TestCase
from django.urls import reverse
from .models import Book, Author, Publisher, Genre, Language


class TestBook(TestCase):
    """Тестирование представлений модели Book"""

    def setUp(self):
        """Предварительное создание данных"""

        self.author = list()
        self.genre = list()
        self.language = list()
        for idx in range(2):
            language = Language.objects.create(title=f"test_language_title_{idx}")
            genre = Genre.objects.create(title=f"test_genre_title_{idx}")
            author = Author.objects.create(
                first_name=f"test_first_name_{idx}",
                last_name=f"test_last_name_{idx}",
                country=f"test_country_{idx}"
            )
            self.author.append(author)
            self.genre.append(genre)
            self.language.append(language)
            self.publisher = Publisher.objects.create(
                title=f"PublisherTitle_{idx}",
                address="PublisherAddress",
                email_address=f"pub{idx}lisher@test.com"
            )
            self.book = Book.objects.create(
                title=f"TitleBook_{idx}",
                publisher=self.publisher,
                pages=200,
                year=2023
            )
            self.book.author.set([aut.pk for aut in self.author])
            self.book.language.set([lang for lang in self.language])
            self.book.genre.set([gen for gen in self.genre])

    def tearDown(self):
        """Удаление данных после завершения теста"""
        Language.objects.all().delete()
        Genre.objects.all().delete()
        Author.objects.all().delete()
        Publisher.objects.all().delete()
        Book.objects.all().delete()

    def test_all_book_views(self):
        """Вывод всех книг"""

        url_book = reverse("home")
        response = self.client.get(url_book)
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, "TitleBook_0")
        self.assertContains(response, "TitleBook_1")
        Book.objects.all().delete()
        response = self.client.get(url_book)
        self.assertEquals(response.status_code, 200)

    def test_pagination(self):
        """Пагинация"""

        url_book = reverse("home")
        response = self.client.get(url_book)
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, "TitleBook_0")
        self.assertNotContains(response, "Next")
        self.assertContains(response, "TitleBook_1")

    def test_add_book(self):
        """Добавление книги"""

        url_book = reverse("add_book")

        data = {"title": "История Postman", "language": [1, 2], "author": [1, 2], "publisher": 1, "genre": [1, 2],
                "pages": 777, "year": 2022
                }
        response = self.client.post(url_book, data)
        self.assertEquals(response.status_code, 200)  # 302 - перенаправление
        self.assertEquals(Book.objects.count(), 2)

    def test_update_book(self):
        """Обновление книги"""

        new_language = Language.objects.create(title="New_Language")
        new_author = Author.objects.create(first_name="New_First_Name", last_name="New_Last_Name",
                                           country="New_Country")
        new_publisher = Publisher.objects.create(title="New_Publisher", address="New_Address",
                                                 email_address="new@test.com")
        new_genre = Genre.objects.create(title="New Genre")

        for obj in Book.objects.all():
            url_book = reverse("update_book", kwargs={"slug": obj.slug})

            update = {
                "title": f"UpdateTitle{obj.pk}",
                "language": [new_language.pk],
                "author": [new_author.pk],
                "publisher": new_publisher.pk,
                "genre": [new_genre.pk],
                "pages": 500,
                "year": 2011
            }

            response = self.client.put(url_book, update)
            self.assertEquals(response.status_code, 200)
            self.assertEquals(Book.objects.count(), 2)
            url_book = reverse("update_book", kwargs={"slug": "test"})
            response = self.client.put(url_book, update)
            self.assertEquals(response.status_code, 404)

    def test_delete_book(self):
        """Удаление книги"""

        for book in Book.objects.all():
            url_book = reverse("delete_book", kwargs={"slug": book.slug})
            response = self.client.delete(url_book)
            self.assertEquals(response.status_code, 302)  # перенаправление
            self.assertFalse(Book.objects.filter(slug=book.slug).exists())

        url_book = reverse("delete_book", kwargs={"slug": "test"})
        response = self.client.delete(url_book)
        self.assertEquals(response.status_code, 404)

    def test_detail_book(self):
        """Получение конкретной книги"""

        for book in Book.objects.all():
            url_book = reverse("detail_book", kwargs={"slug": book.slug})
            response = self.client.get(url_book)
            self.assertEquals(response.status_code, 200)
            self.assertContains(response, Book.objects.get(slug=book.slug).title)

        url_book = reverse("detail_book", kwargs={"slug": "test"})
        response = self.client.get(url_book)
        self.assertEquals(response.status_code, 404)


class TestAuthorAndPublisher(TestCase):
    """Тестирование представлений для модели Author и Publisher"""

    def setUp(self):
        """Предварительное создание данных"""

        self.author = Author.objects.create(
            first_name="TestName",
            last_name="TestLastName",
            country="TestCountry"
        )
        self.publisher = Publisher.objects.create(
            title="TestTitlePublisher",
            address="TestAddress",
            email_address="test@test.com"
        )

    def tearDown(self):
        """Очищает тестовую базу данных"""

        Author.objects.all().delete()
        Publisher.objects.all().delete()

    def test_all_views(self):
        """Вывод всех записей моделей Author и Publisher"""

        url_publisher = reverse("all_publisher")
        url_author = reverse("all_author")

        response_publisher = self.client.get(url_publisher)
        response_author = self.client.get(url_author)
        self.assertEquals(response_publisher.status_code, 200)
        self.assertEquals(response_author.status_code, 200)

        Publisher.objects.all().delete()
        Author.objects.all().delete()

        response_publisher = self.client.get(url_publisher)
        response_author = self.client.get(url_author)
        self.assertEquals(response_publisher.status_code, 200)
        self.assertEquals(response_author.status_code, 200)

    def test_add_data(self):
        """Добавление данных в таблицу"""

        url_publisher = reverse("create_publisher")
        url_author = reverse("add_author")
        add_data_publisher = {
            "title": "NewTitle",
            "address": "New address",
            "email_address": "newtest@test.com"
        }
        add_data_author = {
            "first_name": "NewFirstName",
            "last_name": "NewLastName",
            "country": "NewCountry"
        }
        response_publisher = self.client.post(url_publisher, add_data_publisher)
        response_author = self.client.post(url_author, add_data_author)
        self.assertEquals(response_publisher.status_code, 302)
        self.assertEquals(response_author.status_code, 302)

        self.assertTrue(Publisher.objects.filter(title="NewTitle"))
        self.assertTrue(Author.objects.filter(first_name="NewFirstName"))

    def test_delete(self):
        """Удаление записей из моделей Publisher"""

        for pub in Publisher.objects.all():
            url_publisher = reverse("delete_publisher", kwargs={"slug": pub.slug})
            response_publisher = self.client.delete(url_publisher)
            self.assertEquals(response_publisher.status_code, 302)
            self.assertFalse(Publisher.objects.filter(slug=pub.slug))
            response_publisher = self.client.delete(url_publisher)
            self.assertEquals(response_publisher.status_code, 404)
