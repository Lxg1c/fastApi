from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import sessionmaker

from app.core.config import settings


class DbHelper:

    def __init__(self, url, echo=False):
        self.engine = create_async_engine(
            url=url,
            echo=echo,
        )

        self.session = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )


db_helper = DbHelper(
    url=settings.db_url,
    echo=settings.db_echo,
)
