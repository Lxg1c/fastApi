from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI
from core.config import settings
from core.models import Base
from core.models.db_helper import db_helper
from api_v1 import router as api_v1


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_helper.engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(api_v1, prefix=settings.api_v1_prefix)


@app.get("/")
def hello_index():
    return {"message": "Hello World"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
