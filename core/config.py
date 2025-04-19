from pathlib import Path

from pydantic_settings import BaseSettings

# Определяем базовую директорию проекта
BASE_DIR = Path(__file__).parent.parent


# Настройки базы данных
class DbSettings(BaseSettings):
    # URL подключения к базе (SQLite по умолчанию)
    url: str = f"sqlite+aiosqlite:///{BASE_DIR}/db.sqlite3"
    # Логировать SQL-запросы
    echo: bool = False


# Настройки JWT-аутентификации
class AuthJWT(BaseSettings):
    # Пути к RSA-ключам
    private_key_path: Path = BASE_DIR / "certs" / "jwt-private.pem"
    public_key_path: Path = BASE_DIR / "certs" / "jwt-public.pem"
    algorithm: str = "RS256"
    # Время жизни access-токена (в минутах)
    access_token_expire_minutes: int = 60
    # Время жизни refresh-токена (в минутах)
    refresh_token_expire_minutes: int = 30 * 60 * 24


# Общие настройки приложения
class Settings(BaseSettings):
    # Префикс для API
    api_v1_prefix: str = "/api/v1"
    # Вложенные настройки базы и JWT
    db: DbSettings = DbSettings()
    auth_jwt: AuthJWT = AuthJWT()


# Экземпляр настроек, который можно импортировать в других модулях
settings = Settings()
