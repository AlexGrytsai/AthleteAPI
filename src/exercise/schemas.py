from enum import Enum
from typing import Annotated
from typing import Optional

from annotated_types import MaxLen, MinLen
from pydantic import BaseModel, HttpUrl


class EquipmentType(str, Enum):
    BARBELL = "Barbell"
    DUMBBELLS = "Dumbbells"
    DUMBBELL = "Dumbbell"
    KETTLEBELL = "Kettlebell"
    OTHER = "Other"


class BodyPart(str, Enum):
    UPPER_BODY = "Upper body"
    LOWER_BODY = "Lower body"
    CORE = "Core"


class MainUpperMuscles(str, Enum):
    PECTORAL_MUSCLES = "Pectoral muscles"
    SHOULDERS = "Shoulders"
    BICEPS = "Biceps"
    TRICEPS = "Triceps"
    FOREARMS = "Forearms"
    TRAPS = "Traps"
    LATS = "Lats"


class MainLowerMuscles(str, Enum):
    QUADRICEPS = "Quadriceps"
    HAMSTRINGS = "Hamstrings"
    CALVES = "Calves"
    GLUTES = "Glutes"


class ExerciseCreate(BaseModel):
    name: Annotated[str, MaxLen(100), MinLen(5)]
    body_part: BodyPart
    target_muscles: Annotated[str, MaxLen(100), MinLen(5)]
    additional_muscle: Optional[Annotated[str, MaxLen(100), MinLen(5)]] = None
    description: Optional[Annotated[str, MaxLen(1000), MinLen(30)]] = (
        "No description provided"
    )
    execution_description: Optional[
        Annotated[str, MaxLen(1000), MinLen(30)]
    ] = "No execution description provided"
    image_url: Optional[HttpUrl] = None
    video_url: Optional[HttpUrl] = None
    is_own_weight: bool = False
    if not is_own_weight:
        equipment_type: EquipmentType
