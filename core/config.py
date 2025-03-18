from pydantic_settings import BaseSettings
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent


class DbSettings(BaseSettings):
    url: str = f"sqlite+aiosqlite:///{BASE_DIR}/db.sqlite3"
    echo: bool = True


class AuthJWT(BaseSettings):
    # Генерация приватного ключа RSA 2048 бит
    # openssl genpkey -algorithm RSA -out certs/jwt-private.pem
    private_key_path: Path = BASE_DIR / "certs" / "jwt-private.pem"
    # Генерация публичного ключа из приватного
    # openssl rsa -in certs/jwt-private.pem -pubout -out certs/jwt-public.pem
    public_key_path: Path = BASE_DIR / "certs" / "jwt-public.pem"
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 30


class Settings(BaseSettings):
    api_v1_prefix: str = "/api/v1"

    db: DbSettings = DbSettings()

    auth_jwt: AuthJWT = AuthJWT()


settings = Settings()
