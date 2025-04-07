from asyncio import current_task
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
    async_scoped_session,
)

from core.config import settings


class DatabaseHelper:
    def __init__(self, url: str, echo: bool = False):
        # Создание асинхронного движка SQLAlchemy
        self.engine = create_async_engine(
            url=url,
            echo=echo,  # Логировать SQL-запросы (удобно для отладки)
        )

        # Фабрика сессий (аналог SessionLocal), управляет жизненным циклом сессий
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,  # Не выполнять автоматический flush перед запросами
            autocommit=False,  # Явное управление транзакциями
            expire_on_commit=False,  # Сохранять данные в объекте после коммита
        )

    def get_scoped_session(self) -> async_scoped_session:
        # Возвращает "сессию с областью видимости" — привязанную к текущей задаче asyncio
        session = async_scoped_session(
            session_factory=self.session_factory,
            scopefunc=current_task,  # Используем текущую задачу как область видимости
        )
        return session

    async def scoped_session_dependency(self) -> AsyncGenerator[AsyncSession, None]:
        # FastAPI-зависимость, использующая scoped session
        scoped_session = self.get_scoped_session()
        async with scoped_session() as session:
            yield session  # Передаем сессию в обработчик запроса
            # Автоматически закроется после выхода из блока

    async def session_dependency(self) -> AsyncGenerator[AsyncSession, None]:
        # Альтернативная зависимость — напрямую из фабрики, без области видимости
        async with self.session_factory() as session:
            yield session
            # Также автоматически закроется после выхода из блока


# Создаем объект помощника базы данных с настройками из конфигурации
db_helper = DatabaseHelper(
    url=settings.db.url,
    echo=settings.db.echo,
)
