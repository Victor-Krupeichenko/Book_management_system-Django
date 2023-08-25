from rest_framework.test import APITestCase
from django.urls import reverse
from book_management.models import Language, Genre


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
