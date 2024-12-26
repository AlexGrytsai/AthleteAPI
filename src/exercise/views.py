from typing import Annotated, List

from fastapi import APIRouter, Path

from src.exercise.schemas import ExerciseCreate

router = APIRouter(prefix="/api/v1/exercises")


@router.get("/")
def get_list_exercises() -> List[Exercise]:
    pass


@router.get("/{exercise_name}/")
def get_exercise_detail(
    exercise_name: Annotated[
        str, Path(title="The name of the exercise to get", max_length=100)
    ]
) -> ExerciseCreate:
    pass
