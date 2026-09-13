# Bulletin board (Backend)
Backend доски объявлений на Django REST Framework. (Работа над фронтом в процессе) Позволяет пользователям регистрироваться, 
публиковать объявления, оставлять отзывы к объявлениям пользователей с учетом разделения прав доступа.  

- **Аноним** — может просматривать список объявлений
- **Авторизованный пользователь** — может просматривать, создавать объявления/отзывы, 
  редактировать и удалять только свои
- **Администратор** — дополнительно может редактировать/удалять объявления и отзывы любых пользователей

# Технологии

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![DRF](https://img.shields.io/badge/DRF-A30000?style=for-the-badge&logo=django&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![JWT](https://img.shields.io/badge/JWT-000000?style=for-the-badge&logo=jsonwebtokens&logoColor=white)
![Git](https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white)
![Swagger](https://img.shields.io/badge/Swagger-85EA2D?style=for-the-badge&logo=swagger&logoColor=black)

# Требования к установке
- Python 3.12+
- Poetry
- Docker
# Установка проекта

## Контейнер для базы данных, но приложение локально (для ускорения разработки)

1) Клонируйте репозиторий ```git clone -b develop https://github.com/MrProdeon/bulletin_board.git```
2) Установите poetry ```pip install poetry```
3) Установите зависимости ```poetry install --no-root```
4) Заполните .env файл по примеру из .env.template
5) Запустите Docker Desktop и выполните команду ```docker-compose up -d db```
6) Запустите локальный сервер ```python manage.py runserver```
7) Локальный сервер готов принимать запросы по адресу http://127.0.0.1:8000/

## Локально с использованием docker для базы данных и приложения
1) Выполните шаги с 1 по 4 включительно из инструкции выше
2) Выполните команду docker-compose up --build (флаг --build обязателен для первого запуска и при изменениях в зависимостях,
в остальных случаях можно убрать этот флаг)
3) Сервер будет доступен локально по адресу http://127.0.0.1:8000/
   (При запуске через Docker автоматически переопределяются переменные окружения 
   DB_HOST становится db, DB_PORT будет 5432. Это нужно для того, 
   чтобы контейнер web мог обращаться к db внутри Docker-сети)  

## На удалённом сервере

В процессе описания, функционал ещё не готов  


# Документация методов проекта

## Локальный запуск

При локальном запуске документация будет находиться по адресу :
- Swagger - http://127.0.0.1:8000/swagger/
- Redoc - http://127.0.0.1:8000/redoc/

## Удалённый сервер
При запуске на удалённом сервере документация будет находиться по адресу :

- Swagger - http://your_ip_adress/swagger/
- Redoc - http://your_ip_adress/redoc/

# Тесты
 
Для проекта были написаны тесты с использованием `pytest` и `pytest-django`.
Правила для запуска тестов описаны в файле `.coveragerc`.
Тесты покрывают приложения `users`, `ads`, `reviews`.
 
- Запуск всех тестов ```pytest```
- Запуск тестов конкретного приложения ```pytest users``` (например, `ads` или `reviews`)
- Запуск конкретного теста ```pytest users/test_users_pytest.py::TestCustomUserAPI::test_users_list```
- Запуск с подробным выводом ```pytest -v```  

Запуск тестов с отчётом о покрытии:
```
pytest --cov=users --cov=ads --cov=reviews --cov-report=html
```
Отчёт можно просмотреть в папке `htmlcov` → `index.html`
 

Для ручного тестирования вы можете использовать админку.  
Чтобы попасть в неё - вам необходимо создать суперпользователя с помощью команды
```python manage.py createsuperuser``` и перейти по адресу http://127.0.0.1:8000/admin/

