# Payment Aggregator API

[English](#english) | [Русский](#russian)

---

## English

A production-ready payment aggregation platform built with FastAPI, designed to handle multiple payment providers through a unified API interface.

### Architecture

This project implements a modern microservices-oriented architecture with clear separation of concerns:

- **API Layer**: RESTful endpoints with OpenAPI documentation
- **Service Layer**: Business logic and payment processing
- **Data Layer**: SQLAlchemy ORM with PostgreSQL
- **Task Queue**: Celery workers for asynchronous operations
- **Integration Layer**: Pluggable payment provider system

### Tech Stack

- **Framework**: FastAPI 0.115.0
- **Database**: PostgreSQL with SQLAlchemy 2.0
- **Migrations**: Alembic
- **Authentication**: JWT with bcrypt password hashing
- **Task Queue**: Celery with Redis broker
- **Payment Providers**: Stripe (extensible architecture)
- **Testing**: pytest with async support

### Project Structure

```
app/
├── api/
│   ├── routes/          # API endpoints
│   │   ├── auth.py      # Authentication endpoints
│   │   ├── payments.py  # Payment operations
│   │   └── merchant.py  # Merchant management
│   └── deps.py          # Dependency injection
├── core/
│   ├── config.py        # Application configuration
│   ├── database.py      # Database connection
│   └── security.py      # Security utilities
├── models/              # SQLAlchemy models
│   ├── merchant.py
│   ├── transaction.py
│   └── webhook.py
├── schemas/             # Pydantic schemas
│   ├── merchant.py
│   └── transaction.py
├── services/            # Business logic
│   └── payment_service.py
├── integrations/        # Payment provider integrations
│   ├── base.py
│   └── stripe_provider.py
├── tasks/               # Celery tasks
│   ├── celery_app.py
│   ├── payment_tasks.py
│   └── webhook_tasks.py
└── main.py              # Application entry point
```

### Features

#### Authentication & Authorization
- JWT-based authentication with secure token generation
- Bcrypt password hashing with configurable rounds
- API key generation for merchant integrations
- Role-based access control

#### Payment Processing
- Multi-provider payment support (currently Stripe)
- Asynchronous payment status tracking
- Transaction lifecycle management
- Automatic retry logic for failed operations

#### Webhook System
- Configurable webhook endpoints per merchant
- HMAC signature verification
- Automatic retry with exponential backoff
- Comprehensive webhook delivery logging

#### Database
- PostgreSQL with connection pooling
- Alembic migrations for schema versioning
- Proper indexing on frequently queried fields
- Relationship management with SQLAlchemy ORM

### Installation

#### Prerequisites
- Python 3.12+
- PostgreSQL 14+
- Redis 6+

#### Setup

1. Clone the repository:
```bash
git clone https://github.com/nezxenka/payment-aggregator.git
cd payment-aggregator
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. Run database migrations:
```bash
alembic upgrade head
```

5. Start the application:
```bash
uvicorn app.main:app --reload
```

6. Start Celery worker (in separate terminal):
```bash
celery -A app.tasks.celery_app worker --loglevel=info
```

### Configuration

Key environment variables in `.env`:

```env
DATABASE_URL=postgresql+psycopg://user:password@localhost:5432/dbname
REDIS_URL=redis://localhost:6379/0
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret
STRIPE_API_KEY=sk_test_your_stripe_key
```

### API Documentation

Once running, access interactive API documentation:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

#### Core Endpoints

**Authentication**
- `POST /auth/register` - Register new merchant
- `POST /auth/login` - Authenticate and receive JWT token

**Payments**
- `POST /payments/` - Create new payment
- `GET /payments/` - List merchant transactions

**Merchant**
- `GET /merchant/me` - Get current merchant profile
- `POST /merchant/api-key` - Generate new API key

### Usage Example

```python
import httpx

# Register merchant
response = httpx.post("http://localhost:8000/auth/register", json={
    "email": "merchant@example.com",
    "company_name": "My Company",
    "password": "secure_password"
})

# Login
response = httpx.post("http://localhost:8000/auth/login", json={
    "email": "merchant@example.com",
    "password": "secure_password"
})
token = response.json()["access_token"]

# Create payment
headers = {"Authorization": f"Bearer {token}"}
response = httpx.post("http://localhost:8000/payments/", 
    headers=headers,
    json={
        "amount": 100.00,
        "currency": "USD",
        "provider": "stripe",
        "description": "Product purchase",
        "customer_email": "customer@example.com"
    }
)
```

### Database Schema

#### Merchants
- User accounts with authentication credentials
- Balance tracking
- API key management
- Account status flags

#### Transactions
- Payment records with provider details
- Status tracking (pending, processing, completed, failed, refunded)
- Amount and currency information
- Customer metadata

#### Webhooks
- Endpoint configuration per merchant
- Delivery logs with retry tracking
- HMAC signature secrets

### Development

#### Running Tests
```bash
pytest
```

#### Creating New Migration
```bash
alembic revision --autogenerate -m "Description"
alembic upgrade head
```

#### Code Quality
- Type hints throughout the codebase
- Pydantic models for request/response validation
- Dependency injection pattern
- Separation of concerns

### Security Considerations

- Passwords hashed with bcrypt
- JWT tokens with configurable expiration
- API keys hashed before storage
- CORS configuration for cross-origin requests
- SQL injection prevention via ORM
- Input validation with Pydantic

### Deployment

For production deployment:

1. Set `ENVIRONMENT=production` in `.env`
2. Use strong secrets for all keys
3. Configure proper CORS origins
4. Set up SSL/TLS termination
5. Use connection pooling for database
6. Configure Celery with proper concurrency
7. Set up monitoring and logging

### License

MIT

---

## Russian

Готовая к продакшену платформа для агрегации платежей, построенная на FastAPI и предназначенная для работы с несколькими платежными провайдерами через единый API интерфейс.

### Архитектура

Проект реализует современную микросервисную архитектуру с четким разделением ответственности:

- **API слой**: RESTful эндпоинты с OpenAPI документацией
- **Сервисный слой**: Бизнес-логика и обработка платежей
- **Слой данных**: SQLAlchemy ORM с PostgreSQL
- **Очередь задач**: Celery воркеры для асинхронных операций
- **Слой интеграций**: Подключаемая система платежных провайдеров

### Технологический стек

- **Фреймворк**: FastAPI 0.115.0
- **База данных**: PostgreSQL с SQLAlchemy 2.0
- **Миграции**: Alembic
- **Аутентификация**: JWT с bcrypt хешированием паролей
- **Очередь задач**: Celery с Redis брокером
- **Платежные провайдеры**: Stripe (расширяемая архитектура)
- **Тестирование**: pytest с поддержкой async

### Структура проекта

```
app/
├── api/
│   ├── routes/          # API эндпоинты
│   │   ├── auth.py      # Эндпоинты аутентификации
│   │   ├── payments.py  # Операции с платежами
│   │   └── merchant.py  # Управление мерчантами
│   └── deps.py          # Dependency injection
├── core/
│   ├── config.py        # Конфигурация приложения
│   ├── database.py      # Подключение к БД
│   └── security.py      # Утилиты безопасности
├── models/              # SQLAlchemy модели
│   ├── merchant.py
│   ├── transaction.py
│   └── webhook.py
├── schemas/             # Pydantic схемы
│   ├── merchant.py
│   └── transaction.py
├── services/            # Бизнес-логика
│   └── payment_service.py
├── integrations/        # Интеграции с платежными провайдерами
│   ├── base.py
│   └── stripe_provider.py
├── tasks/               # Celery задачи
│   ├── celery_app.py
│   ├── payment_tasks.py
│   └── webhook_tasks.py
└── main.py              # Точка входа приложения
```

### Возможности

#### Аутентификация и авторизация
- JWT-аутентификация с безопасной генерацией токенов
- Bcrypt хеширование паролей с настраиваемыми раундами
- Генерация API ключей для интеграций мерчантов
- Контроль доступа на основе ролей

#### Обработка платежей
- Поддержка нескольких провайдеров (сейчас Stripe)
- Асинхронное отслеживание статуса платежей
- Управление жизненным циклом транзакций
- Автоматическая логика повторных попыток при ошибках

#### Система вебхуков
- Настраиваемые webhook эндпоинты для каждого мерчанта
- HMAC верификация подписей
- Автоматические повторы с экспоненциальной задержкой
- Полное логирование доставки вебхуков

#### База данных
- PostgreSQL с пулом соединений
- Alembic миграции для версионирования схемы
- Правильная индексация часто запрашиваемых полей
- Управление связями через SQLAlchemy ORM

### Установка

#### Требования
- Python 3.12+
- PostgreSQL 14+
- Redis 6+

#### Настройка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/nezxenka/payment-aggregator.git
cd payment-aggregator
```

2. Установите зависимости:
```bash
pip install -r requirements.txt
```

3. Настройте переменные окружения:
```bash
cp .env.example .env
# Отредактируйте .env с вашей конфигурацией
```

4. Запустите миграции базы данных:
```bash
alembic upgrade head
```

5. Запустите приложение:
```bash
uvicorn app.main:app --reload
```

6. Запустите Celery воркер (в отдельном терминале):
```bash
celery -A app.tasks.celery_app worker --loglevel=info
```

### Конфигурация

Ключевые переменные окружения в `.env`:

```env
DATABASE_URL=postgresql+psycopg://user:password@localhost:5432/dbname
REDIS_URL=redis://localhost:6379/0
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret
STRIPE_API_KEY=sk_test_your_stripe_key
```

### Документация API

После запуска доступна интерактивная документация API:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

#### Основные эндпоинты

**Аутентификация**
- `POST /auth/register` - Регистрация нового мерчанта
- `POST /auth/login` - Аутентификация и получение JWT токена

**Платежи**
- `POST /payments/` - Создание нового платежа
- `GET /payments/` - Список транзакций мерчанта

**Мерчант**
- `GET /merchant/me` - Получение профиля текущего мерчанта
- `POST /merchant/api-key` - Генерация нового API ключа

### Пример использования

```python
import httpx

# Регистрация мерчанта
response = httpx.post("http://localhost:8000/auth/register", json={
    "email": "merchant@example.com",
    "company_name": "Моя Компания",
    "password": "secure_password"
})

# Логин
response = httpx.post("http://localhost:8000/auth/login", json={
    "email": "merchant@example.com",
    "password": "secure_password"
})
token = response.json()["access_token"]

# Создание платежа
headers = {"Authorization": f"Bearer {token}"}
response = httpx.post("http://localhost:8000/payments/", 
    headers=headers,
    json={
        "amount": 100.00,
        "currency": "USD",
        "provider": "stripe",
        "description": "Покупка товара",
        "customer_email": "customer@example.com"
    }
)
```

### Схема базы данных

#### Merchants (Мерчанты)
- Учетные записи пользователей с учетными данными
- Отслеживание баланса
- Управление API ключами
- Флаги статуса аккаунта

#### Transactions (Транзакции)
- Записи платежей с деталями провайдера
- Отслеживание статуса (pending, processing, completed, failed, refunded)
- Информация о сумме и валюте
- Метаданные клиента

#### Webhooks (Вебхуки)
- Конфигурация эндпоинтов для каждого мерчанта
- Логи доставки с отслеживанием повторов
- Секреты для HMAC подписей

### Разработка

#### Запуск тестов
```bash
pytest
```

#### Создание новой миграции
```bash
alembic revision --autogenerate -m "Описание"
alembic upgrade head
```

#### Качество кода
- Type hints во всей кодовой базе
- Pydantic модели для валидации запросов/ответов
- Паттерн dependency injection
- Разделение ответственности

### Соображения безопасности

- Пароли хешируются с помощью bcrypt
- JWT токены с настраиваемым временем истечения
- API ключи хешируются перед сохранением
- CORS конфигурация для cross-origin запросов
- Защита от SQL инъекций через ORM
- Валидация входных данных с Pydantic

### Деплой

Для продакшен деплоя:

1. Установите `ENVIRONMENT=production` в `.env`
2. Используйте сильные секреты для всех ключей
3. Настройте правильные CORS origins
4. Настройте SSL/TLS терминацию
5. Используйте connection pooling для базы данных
6. Настройте Celery с правильной конкурентностью
7. Настройте мониторинг и логирование

### Лицензия

MIT

### Автор

Портфолио проект backend разработчика, демонстрирующий работу с FastAPI, PostgreSQL, Celery и интеграцией платежных систем.