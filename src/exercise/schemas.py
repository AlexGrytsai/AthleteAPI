from typing import Annotated
from typing import Optional

from annotated_types import MaxLen, MinLen
from pydantic import BaseModel, HttpUrl


class Exercise(BaseModel):
    name: Annotated[str, MaxLen(100), MinLen(5)]
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
