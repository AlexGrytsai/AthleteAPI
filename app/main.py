from typing import Annotated

from fastapi import FastAPI, Path

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI with Poetry!"}


@app.get("api/v1/exercises")
def get_list_exercises():
    return ["Exercise 1", "Exercise 2", "Exercise 3"]

@app.get("api/v1/exercises/{exercise_name}")
def get_exercise_detail(exercise_name: Annotated[str, Path(title="The name of the exercise to get")]):
    return f"Exercise {exercise_name}"