from rest_framework.test import APITestCase
from django.urls import reverse
from book_management.models import Language, Genre, Author, Publisher, Book


class TestLanguageAndGenre(APITestCase):
    """Класс для тестирования представлений для Языка(Language) книги и Жанра(Genre) книги"""

    url_language_create = reverse("api:add_language")
    url_genre_create = reverse("api:add_genre")
    url_language_show_all = reverse("api:list_language")
    url_genre_show_all = reverse("api:list_genre")

    def setUp(self):
        """Наполняет тестовую базу данных данными"""

        languages_data = ["Русский", "Польский", "Беларусский"]
        genres_data = ["Триллер", "Фантастика", "Боевик"]
        self.languages = list()
        self.genres = list()
        for i in range(3):
            language = Language.objects.create(title=languages_data[i])
            genre = Genre.objects.create(title=genres_data[i])
            self.languages.append(language)
            self.genres.append(genre)

    def tearDown(self):
        """Очищает тестовую базу данных после завершения тестов"""

        Language.objects.all().delete()
        Genre.objects.all().delete()

    def test_all_list_views(self):
        """Показ всех данных"""

        response_language = self.client.get(self.url_language_show_all)
        response_genre = self.client.get(self.url_genre_show_all)

        self.assertEquals(response_language.status_code, 200)
        self.assertEquals(response_genre.status_code, 200)

        for idx in range(len(self.languages)):
            self.assertEquals(response_language.data[idx]["title"], self.languages[idx].title)
            self.assertEquals(response_genre.data[idx]["title"], self.genres[idx].title)

        Language.objects.all().delete()
        Genre.objects.all().delete()
        response_language = self.client.get(self.url_language_show_all)
        response_genre = self.client.get(self.url_genre_show_all)
        self.assertEquals(response_language.status_code, 200)
        self.assertEquals(response_genre.status_code, 200)
        self.assertEquals(response_language.data, [])
        self.assertEquals(response_genre.data, [])

    def test_put_update(self):
        """Обновление записи"""

        for obj in Language.objects.all():
            url_language = reverse("api:update_language", kwargs={"pk": obj.pk})
            url_genre = reverse("api:update_genre", kwargs={"pk": obj.pk})
            data_update = {
                "title": f"Test_{obj.title}"
            }
            response_language = self.client.put(url_language, data_update)
            response_genre = self.client.put(url_genre, data_update)

            self.assertEquals(response_language.status_code, 200)
            self.assertEquals(response_genre.status_code, 200)
            self.assertEquals(Language.objects.get(pk=obj.pk).title, f"Test_{obj.title}")
            self.assertEquals(Genre.objects.get(pk=obj.pk).title, f"Test_{obj.title}")

            response_language = self.client.put(url_language, {})
            response_genre = self.client.put(url_genre, {})
            self.assertEquals(response_language.status_code, 400)
            self.assertEquals(response_genre.status_code, 400)

        url_language = reverse("api:update_language", kwargs={"pk": 100})
        url_genre = reverse("api:update_genre", kwargs={"pk": 100})
        data_update = {
            "title": f"Test_test"
        }
        response_language = self.client.put(url_language, data_update)
        response_genre = self.client.put(url_genre, data_update)
        self.assertEquals(response_language.status_code, 404)
        self.assertEquals(response_genre.status_code, 404)

    def test_add_data(self):
        """Добавление данных(создание записей в базе данных)"""

        for i in range(3):
            add_data = {
                "title": f"Add_title_{i}"
            }
            response_language = self.client.post(self.url_language_create, add_data)
            response_genre = self.client.post(self.url_genre_create, add_data)
            self.assertEquals(response_language.status_code, 201)
            self.assertEquals(response_genre.status_code, 201)

            response_language = self.client.post(self.url_language_create, add_data)
            response_genre = self.client.post(self.url_genre_create, add_data)
            self.assertEquals(response_language.status_code, 400)
            self.assertEquals(response_genre.status_code, 400)

        response_language = self.client.post(self.url_language_create, {})
        response_genre = self.client.post(self.url_genre_create, {})
        self.assertEquals(response_language.status_code, 400)
        self.assertEquals(response_genre.status_code, 400)

    def test_delete_data(self):
        """Удаление данных"""

        for language, genre in zip(self.languages, self.genres):
            url_language = reverse("api:delete_language", kwargs={"pk": language.pk})
            url_genre = reverse("api:delete_genre", kwargs={"pk": genre.pk})

            response_language = self.client.delete(url_language)
            response_genre = self.client.delete(url_genre)

            self.assertEquals(response_language.status_code, 204)
            self.assertEquals(response_genre.status_code, 204)
            self.assertFalse(Language.objects.filter(pk=language.pk).exists())
            self.assertFalse(Genre.objects.filter(pk=genre.pk).exists())

            response_language = self.client.delete(url_language)
            response_genre = self.client.delete(url_genre)
            self.assertEquals(response_language.status_code, 404)
            self.assertEquals(response_genre.status_code, 404)


class TestPublisherAndAuthor(APITestCase):
    """Тестирование представлений моделей Publisher и Author"""

    def setUp(self):
        """Создание тестовых данных"""

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

        url_publisher = reverse("api:list_publisher")
        url_author = reverse("api:list_author")

        response_publisher = self.client.get(url_publisher)
        response_author = self.client.get(url_author)
        self.assertEquals(response_publisher.status_code, 200)
        self.assertEquals(response_author.status_code, 200)

        Publisher.objects.all().delete()
        Author.objects.all().delete()

        response_publisher = self.client.get(url_publisher)
        response_author = self.client.get(url_author)
        self.assertEquals(response_publisher.data, [])
        self.assertEquals(response_author.data, [])

    def test_add_data(self):
        """Добавление данных в таблицу"""

        url_publisher = reverse("api:add_publisher")
        url_author = reverse("api:add_author")
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
        self.assertEquals(response_publisher.status_code, 201)
        self.assertEquals(response_author.status_code, 201)

        self.assertTrue(Publisher.objects.filter(title="NewTitle"))
        self.assertTrue(Author.objects.filter(first_name="NewFirstName"))

        response_publisher = self.client.post(url_publisher, {})
        response_author = self.client.post(url_author, {})
        self.assertEquals(response_publisher.status_code, 400)
        self.assertEquals(response_author.status_code, 400)

        response_publisher = self.client.post(url_publisher, {"title": "OneField"})
        response_author = self.client.post(url_author, {"first_name": "OneField"})
        self.assertEquals(response_publisher.status_code, 400)
        self.assertEquals(response_author.status_code, 400)

    def test_delete(self):
        """Удаление записей из моделей Publisher и Author"""

        for pub, aut in zip(Publisher.objects.all(), Author.objects.all()):
            url_publisher = reverse("api:delete_publisher", kwargs={"pk": pub.pk})
            url_author = reverse("api:delete_author", kwargs={"pk": aut.pk})
            response_publisher = self.client.delete(url_publisher)
            response_author = self.client.delete(url_author)
            self.assertEquals(response_publisher.status_code, 204)
            self.assertEquals(response_author.status_code, 204)
            self.assertFalse(Publisher.objects.filter(pk=pub.pk))
            self.assertFalse(Author.objects.filter(pk=aut.pk))

            response_publisher = self.client.delete(url_publisher)
            response_author = self.client.delete(url_author)
            self.assertEquals(response_publisher.status_code, 404)
            self.assertEquals(response_author.status_code, 404)

    def test_put_update(self):
        """Полное обновление записи модели Publisher или Author"""

        for pub, aut in zip(Publisher.objects.all(), Author.objects.all()):
            url_publisher = reverse("api:put_update_publisher", kwargs={"pk": pub.pk})
            url_author = reverse("api:put_update_author", kwargs={"pk": aut.pk})
            update_publisher = {
                "title": "Update_title",
                "address": "Update_address",
                "email_address": "updatetest@tes.com"
            }
            update_author = {
                "first_name": "Update_name",
                "last_name": "Update_last_name",
                "country": "Update_Country"
            }
            response_publisher = self.client.put(url_publisher, update_publisher)
            response_author = self.client.put(url_author, update_author)
            self.assertEquals(response_publisher.status_code, 200)
            self.assertEquals(response_author.status_code, 200)
            self.assertTrue(Publisher.objects.filter(title="Update_title").exists())
            self.assertTrue(Author.objects.filter(first_name="Update_name").exists())

            response_publisher = self.client.put(url_publisher, {"title": "NewUpdate"})
            response_author = self.client.put(url_author, {"first_name": "NewFirst_nameUpdate"})
            self.assertEquals(response_publisher.status_code, 400)
            self.assertEquals(response_author.status_code, 400)

            response_publisher = self.client.put(url_publisher, {})
            response_author = self.client.put(url_author, {})
            self.assertEquals(response_publisher.status_code, 400)
            self.assertEquals(response_author.status_code, 400)

            url_publisher = reverse("api:put_update_publisher", kwargs={"pk": 100})
            url_author = reverse("api:put_update_author", kwargs={"pk": 100})
            response_publisher = self.client.patch(url_publisher, update_publisher)
            response_author = self.client.patch(url_author, update_author)
            self.assertEquals(response_publisher.status_code, 404)
            self.assertEquals(response_author.status_code, 404)

    def test_patch_update(self):
        """Частичное обновление записи из таблицы Publisher и Author"""

        for pub, aut in zip(Publisher.objects.all(), Author.objects.all()):
            url_publisher = reverse("api:patch_update_publisher", kwargs={"pk": pub.pk})
            url_author = reverse("api:patch_update_author", kwargs={"pk": aut.pk})
            update_one_field_publisher = {
                "title": "OneFieldUpdate"
            }
            update_one_field_author = {
                "first_name": "OneFieldUpdate"
            }
            response_publisher = self.client.patch(url_publisher, update_one_field_publisher)
            response_author = self.client.patch(url_author, update_one_field_author)
            self.assertEquals(response_publisher.status_code, 200)
            self.assertEquals(response_author.status_code, 200)

            response_publisher = self.client.patch(url_publisher, {})
            response_author = self.client.patch(url_author, {})
            self.assertEquals(response_publisher.status_code, 200)
            self.assertEquals(response_author.status_code, 200)

            url_publisher = reverse("api:patch_update_publisher", kwargs={"pk": 100})
            url_author = reverse("api:patch_update_author", kwargs={"pk": 100})
            response_publisher = self.client.patch(url_publisher, update_one_field_publisher)
            response_author = self.client.patch(url_author, update_one_field_author)
            self.assertEquals(response_publisher.status_code, 404)
            self.assertEquals(response_author.status_code, 404)


class TestBook(APITestCase):
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
            title="PublisherTitle",
            address="PublisherAddress",
            email_address="publisher@test.com"
        )
        self.book = Book.objects.create(
            title="TitleBook",
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
        """Показать все книги"""

        url_book = reverse("api:list_book")
        response = self.client.get(url_book)
        self.assertEquals(response.status_code, 200)
        Book.objects.all().delete()
        response = self.client.get(url_book)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.data, [])

    def test_add_book(self):
        """Добавление книги"""

        url_book = reverse("api:add_book")

        data = {
            "title": "История Postman",
            "language": [1, 2],
            "author": [1, 2],
            "publisher": 1,
            "genre": [1, 2],
            "pages": 777,
            "year": 2022
        }

        response = self.client.post(url_book, data)
        self.assertEquals(response.status_code, 201)
        self.assertEquals(Book.objects.count(), 2)

        data_invalid = {
            "title": "Invalid Data",
            "author": [1, 2],
            "publisher": 1,
            "genre": [1, 2],
            "pages": 777,
            "year": 2022
        }
        response = self.client.post(url_book, data_invalid)
        self.assertEquals(response.status_code, 400)
        self.assertEquals(Book.objects.count(), 2)
        response = self.client.post(url_book, {})
        self.assertEquals(response.status_code, 400)
        self.assertEquals(Book.objects.count(), 2)

    def test_put_update_book(self):
        """Полное обновление записи book"""

        for obj in Book.objects.all():
            url_book = reverse("api:put_update_book", kwargs={"pk": obj.pk})
            new_language = Language.objects.create(title="New_Language")
            new_author = Author.objects.create(first_name="New_First_Name", last_name="New_Last_Name",
                                               country="New_Country")
            new_publisher = Publisher.objects.create(title="New_Publisher", address="New_Address",
                                                     email_address="new@test.com")
            new_genre = Genre.objects.create(title="New Genre")
            update = {
                "title": "UpdateTitle",
                "language": [new_language.pk],
                "author": [new_author.pk],
                "publisher": new_publisher.pk,
                "genre": [new_genre.pk],
                "pages": 500,
                "year": 2011
            }
            response = self.client.put(url_book, update)
            self.assertEquals(response.status_code, 200)
            self.assertEquals(Book.objects.count(), 1)

            update_invalid_data = {
                "title": "UpdateTitle",
                "language": [new_language.pk],
                "author": [new_author.pk],
                "genre": [new_genre.pk],
                "pages": 500,
                "year": 2011
            }
            response = self.client.put(url_book, update_invalid_data)
            self.assertEquals(response.status_code, 400)

            url_book = reverse("api:put_update_book", kwargs={"pk": 100})
            response = self.client.put(url_book, update)
            self.assertEquals(response.status_code, 404)

    def test_patch_update_book(self):
        """Частичное обновление записи book"""
        for book in Book.objects.all():
            url_book = reverse("api:patch_update_book", kwargs={"pk": book.pk})
            update = {
                "title": "Patch_Update_Title"
            }
            response = self.client.patch(url_book, update)
            self.assertEquals(response.status_code, 200)
            self.assertEquals(Book.objects.get(pk=book.pk).title, "Patch_Update_Title")
            update_invalid = {
                "pages": "test",
            }
            response = self.client.patch(url_book, update_invalid)
            self.assertEquals(response.status_code, 400)

        url_book = reverse("api:patch_update_book", kwargs={"pk": 100})
        response = self.client.patch(url_book, {"title": "Test_Title"})
        self.assertEquals(response.status_code, 404)

    def test_delete_book(self):
        """Удаление объекта book"""

        for book in Book.objects.all():
            url_book = reverse("api:delete_book", kwargs={"pk": book.pk})
            response = self.client.delete(url_book)
            self.assertEquals(response.status_code, 204)
            self.assertFalse(Book.objects.filter(pk=book.pk).exists())

        url_book = reverse("api:delete_book", kwargs={"pk": 100})
        response = self.client.delete(url_book)
        self.assertEquals(response.status_code, 404)

    def test_detail_book(self):
        """Получение конкретной записи book"""

        for book in Book.objects.all():
            url_book = reverse("api:detail_book_view", kwargs={"pk": book.pk})
            response = self.client.get(url_book)
            self.assertEquals(response.status_code, 200)
            self.assertEquals(response.data.get("title"), Book.objects.get(pk=book.pk).title)
            Book.objects.all().delete()
            response = self.client.get(url_book)
            self.assertEquals(response.status_code, 404)
