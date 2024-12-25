from pydantic import BaseModel, HttpUrl
from typing import Optional


class Exercise(BaseModel):
    name: str
    target_muscles: str
    additional_muscle: Optional[str] = None
    description: Optional[str] = "No description provided"
    execution_description: Optional[str] = "No execution description provided"
    image_url: Optional[HttpUrl] = None
    video_url: Optional[HttpUrl] = None
