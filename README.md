# Task Manager

Асинхронный микросервис для управления задачами на FastAPI + PostgreSQL + RabbitMQ.  
Поддерживает создание, получение, отмену задач и асинхронную обработку с помощью фонового воркера.

## Запуск

### Клонировать репозиторий
```bash
git clone https://github.com/your-username/task-manager.git
cd task-manager
```

### Создать .env
```bash
DATABASE_URL=postgresql+asyncpg://postgres:postgres@db:5432/tasks
RABBITMQ_URL=amqp://guest:guest@rabbitmq/
SYNC_DATABASE_URL=postgresql+psycopg2://postgres:postgres@db:5432/tasks
```

### Собрать и запустить проект
```bash
docker-compose up --build -d
```

### Применить миграции Alembic
```bash
docker-compose run --rm web alembic upgrade head
```

### Тестирование
```bash
docker-compose run --rm web pytest
```
