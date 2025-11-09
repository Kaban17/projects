# Budget Tracker API

Функциональный трекер бюджета на Scala 3.

## Быстрый старт

1. Запустите PostgreSQL:
```bash
cd docker && docker-compose up -d
```

2. Запустите приложение:
```bash
sbt run
```

3. API доступен на `http://localhost:8080`

## Примеры запросов

### Регистрация
```bash
curl -X POST http://localhost:8080/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"alice","email":"alice@example.com","password":"pass123"}'
```

### Создание транзакции
```bash
curl -X POST http://localhost:8080/transactions \
  -H "Content-Type: application/json" \
  -H "X-User-Id: <userId>" \
  -d '{"amount":1000,"transactionType":"Income","category":"Salary"}'
```

### Получение отчета
```bash
curl http://localhost:8080/reports/budget -H "X-User-Id: <userId>"
```

## Структура
- `domain/` - Модели
- `repository/` - БД (doobie)
- `service/` - Бизнес-логика
- `http/` - HTTP маршруты
