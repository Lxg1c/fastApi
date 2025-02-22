import uvicorn
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def hello_index():
    return {"message": "Hello World"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)