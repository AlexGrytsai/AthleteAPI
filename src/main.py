from fastapi import FastAPI
from src.exercise.views import router as exercises_router
app = FastAPI()

app.include_router(exercises_router, tags=["Exercises"])


@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI with Poetry!"}
