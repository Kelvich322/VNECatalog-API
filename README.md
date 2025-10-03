# VNE Catalog API

REST API для управления каталогом товаров с использованием FastAPI, PostgreSQL и Docker.

## Функциональность

- `GET /api/v1/products` - Получить список товаров с поиском
- `GET /api/v1/products/{id}` - Получить товар по ID  
- `POST /api/v1/products` - Добавить новый товар
- `DELETE /api/v1/products/{id}` - Удалить товар по ID

### Поиск
- **Поиск по категории** - `GET /api/v1/products?category=Electronics`
- **Поиск по названию** - `GET /api/v1/products?name=laptop`
- **Комбинированный поиск** - `GET /api/v1/productcategory=Electronics&name=apple`

## Стек

- **FastAPI**
- **PostgreSQL**
- **SQLAlchemy**
- **Pydantic**
- **Docker**
- **Poetry**
- **Uvicorn**

## Запуск проекта

### 1. Клонирование репозитория

```bash
git clone https://github.com/Kelvich322/VNECatalog-API.git
cd VNECatalog-API
```
### 2. Запуск через Docker Compose

```bash
docker compose up --build
```
- Бэкенд будет доступен по следующему адресу: http://localhost:8000/api/v1
- Swagger документация будет доступна по адресу: http://localhost:8000/docs

### 3. Остановка приложения

```bash
docker compose down
```

## API Endpoints

- POST /api/v1/products - Создать товар
- GET /api/v1/products - Получить список всех товаров (доступен поиск через query-параметры name и category)
- GET /api/v1/products/{id} - Получить информацию о товаре по его ID
- DELETE /api/v1/products/{id} - Удалить товар

## Docker сервисы

- backend: FastAPI приложение
- db: PostgreSQL база данных

## Запуск тестов

Локально. Необходимы установленные poetry и python. Необходимо установить dev зависимости: 
```bash
cd backend
poetry install --with dev
```
Далее:
```bash
poetry run pytest -v
```
Если возникает проблема с модулем app, выполните:
```bash
export PYTHONPATH=$PWD/backend:$PYTHONPATH
```

## Просмотр логов

```bash 
docker compose logs backend
docker compose logs db
```

## Разработчик

**Backend**
- Кельвич Богдан
