# Book_management_system-Django
![Python](https://img.shields.io/badge/-Python-f1f518?style=flat-square&logo=python)   
![Django](https://img.shields.io/badge/-Django-092E20?style=flat-square&logo=django)
![Django Rest](https://img.shields.io/badge/-DjangoRest-092E20?style=flat-square&logo=django-rest)
![Bootstrap](https://img.shields.io/badge/-Bootstrap-ce62f5?style=flat-square&logo=bootstrap)  
![Docker](https://img.shields.io/badge/-Docker-1de4f2?style=flat-square&logo=docker) 
![Postgresql](https://img.shields.io/badge/-Postgresql-1de4f2?style=flat-square&logo=postgresql)  

Приложение менеджмента книг
* Позволяет добавлять авторов книг
* Позволяет добавлять редакции книг
* Позволяет добавлять жанр книги
* Позволяет добавлять обложку книги(в папке media будут динамически создаваться отдельные папки названием книги в которой и будет храниться обложка книги)
* и др.

Приложение написано на Django и Django Rest Framework
Приложение состоит из двух частей:



## Установка
необходимо создать в корне проекта файл .env в котором указать: POSTGRES_DB=ваше_название_для базы данных POSTGRES_HOST=weather_database POSTGRES_USER=ваше_имя_пользователя POSTGRES_PASSWORD=ваш_пароль POSTGRES_PORT=1223(можете указать другой порт-тогда и в docker-compose.yml необходимо изменить на другой) A_PASSWORD=пароль_администратора
A_NAME=имя_администратора
A_EMAIL=email_администратора
SECRET_KEY=секретный_ключ_для_проекта

## Установка на локальный компьютер
- git clone https://github.com/Victor-Krupeichenko/Book_management_system-Django.git
- pip install -r requirements.txt
- запуск через терминал:  python manage.py runserver
- перейти по ссылке: http://127.0.0.1:8000 

## Установка в docker
- git clone https://github.com/Victor-Krupeichenko/Book_management_system-Django.git
- запуск через терминал(обязательно должны находится в папке проекта): docker compose up или docker-compose up
- перейти по ссылке: http://0.0.0.0:80

## Структура проекта
В папке api находится:
1. сериализатор моделей
2. тесты для endpoints
3. url-маршруты для endpoints
4. вспомогательные классы для избежания дублирования кода
5. представления

В папке book_management(web-приложение):
1. миграции для создания таблиц в базе данных
2. папка static для хранения статических файлов для самого приложения
3. регистрация моделей для страницы администратора
4. формы для получения данных от пользователя
5. миксин для валидации формы и отправки уведомления(сообщения) пользователю
6. модели таблиц базы данных
7. тесты для endpoints
8. rl-маршруты для endpoints
9. вспомогательный класс для избежания дублирования кода
10. представление

В папке book_management_system находятся глобальные настройки для проекта
* подключение базы данных, подключение статических и медиа файлов, подключение маршрутов web-приложения и api-приложения и др.

В папке docker_start(предназначена для работы в docker) находится:
* bash-скрипт для проведения миграции для создания таблиц в базе данных, сбора статических файлов, создание суперпользователя и сам запуск приложения

В папке templates находятся:
* папка _inc - содержит подключаемые html-шаблоны
* папка book_management - содержит основные html-шаблоны
* базовый html-шаблон который наследуют html-шаблоны из папки book_management

- docker-compose.yml содержит описание запуска проекта в docker
- Dockerfile содержит инструкции для создания docker-образа
- manage.py - утилита для управления проектом
- nginx.conf - настройки сервера nginx так как django в режиме DEBUG=False не может самостоятельно самостоятельно работать со статическими файлами
- requirements.txt в нем находятся все необходимые для работы приложения библиотеки и зависимости
- setting_env.py - настройки имен переменно окружения

## Контакты:
Виктор
# Email:
- krupeichenkovictor@gmail.com
- victor_krupeichenko@hotmail.com
# Viber:
- +375447031953 
