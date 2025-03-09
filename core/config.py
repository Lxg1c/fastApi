from pydantic_settings import BaseSettings
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent


class Settings(BaseSettings):
    api_v1_prefix: str = "/api/v1"

    db: DbSettings = DbSettings()

    auth_jwt: AuthJWT = AuthJWT()


settings = Settings()
