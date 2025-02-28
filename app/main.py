from contextlib import asynccontextmanager
from core.models import Base
from core.models.db_helper import db_helper
import uvicorn
from fastapi import FastAPI
from views.user import router as user_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_helper.engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(user_router)


@app.get("/")
def hello_index():
    return {"message": "Hello World"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
