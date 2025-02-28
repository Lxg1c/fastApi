from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    db_url: str = "sqlite+aiosqlite:///../database.sqlite"
    db_echo: bool = False


settings = Settings()
