from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api_v1 import router as api_v1
from core.config import settings
from core.models import Base
from core.models.db_helper import db_helper


# Контекст жизненного цикла приложения: создаёт таблицы при старте
@asynccontextmanager
async def lifespan(_: FastAPI):
    # Автоматически создаём таблицы в БД при запуске
    async with db_helper.engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    yield


# Создаём экземпляр FastAPI с указанным жизненным циклом
app = FastAPI(lifespan=lifespan)

# Разрешённые источники для CORS (например, фронтенд на React)
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:3000"
]

# Добавляем middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем маршруты из api_v1 с префиксом /api/v1
app.include_router(api_v1, prefix=settings.api_v1_prefix)

# Точка входа при запуске через python main.py
if __name__ == "__main__":
    # Запуск uvicorn с hot-reload для разработки
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
