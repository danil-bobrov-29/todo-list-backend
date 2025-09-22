# Todo List Backend (FastAPI)

Минималистичный бэкенд для списка задач (To‑Do). Проект написан на Python и предоставляет REST API для CRUD‑операций над задачами.
---

## Стек

* **Python 3.11+**
* **FastAPI** — web‑фреймворк
* **Uvicorn** — ASGI‑сервер
* **SQLAlchemy** — ORM
* **Alembic** — миграции БД
* **Poetry** — менеджер зависимостей

Структура репозитория (ключевые файлы):

```
src/                  # исходный код приложения (например, src/main.py, src/models.py, src/routers/...)
pyproject.toml        # конфигурация Poetry и метаданные проекта
alembic.ini           # конфиг Alembic
.env                  # переменные окружения (локально)
```

---

## Быстрый старт

### 1) Клонирование и установка зависимостей

```bash
git clone https://github.com/danil-bobrov-29/todo-list-backend.git
cd todo-list-backend

# Установка Poetry (если ещё нет)
# https://python-poetry.org/docs/#installation

poetry install
```

### 2) Конфигурация окружения

Создайте файл `.env` в корне проекта и заполните переменные:

```dotenv
APP_NAME=   # Название приложения
APP_VERSION=  # Версия приложения
APP_HOST= # Хост на котором находиться приложение
APP_PORT= # Порт на котором находиться приложение

DATABASE_HOST=  # Хост на подключение в БД
DATABASE_PORT=  # Порт на подключение в БД
DATABASE_USER=  # Пользователь БД
DATABASE_PASSWORD=  # Пароль от пользователя БД
DATABASE_NAME=  # Название БД 

SECURITY_JWT_SECRET=  # Секретный ключ
SECURITY_JWT_ALGORITHM= # Алгоритм шифрования
SECURITY_JWT_ACCESS_TTL_MIN=  # Время жизни access токена (минуты)
SECURITY_JWT_REFRESH_TTL_DAYS=  # Время жизни refresh токена (дней)
```

Примеры строк подключения:

* **SQLite (локально, файл рядом с проектом):** `sqlite+aiosqlite:///./app.db`
* **PostgreSQL:** `postgresql+asyncpg://USER:PASSWORD@HOST:5432/DBNAME`

### 3) Миграции базы данных

```bash
# Инициализация схемы
poetry run alembic upgrade head

# Если меняли модели — создайте новую ревизию и примените её
poetry run alembic revision --autogenerate -m "update models"
poetry run alembic upgrade head
```

### 4) Запуск приложения

```bash
poetry run uvicorn src.main:app --reload --host ${APP_HOST:-0.0.0.0} --port ${APP_PORT:-8000}
```

После старта:

* Swagger‑документация: \`[http://localhost:8000/docs](http://localhost:8000/docs)
