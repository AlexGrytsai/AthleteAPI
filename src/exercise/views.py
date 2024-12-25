from typing import Annotated, List

from fastapi import APIRouter, Path

from src.exercise.schemas import Exercise

router = APIRouter(prefix="/api/v1/exercises")


@router.get("/")
def get_list_exercises() -> List[Exercise]:
    return ["Exercise 1", "Exercise 2", "Exercise 3"]


@router.get("/{exercise_name}/")
def get_exercise_detail(
    exercise_name: Annotated[
        str, Path(title="The name of the exercise to get", max_length=100)
    ]
) -> Exercise:
    return f"Exercise {exercise_name}"
