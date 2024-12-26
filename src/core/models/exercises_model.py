from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.core.models.base import Base


class ExerciseModel(Base):
    name: Mapped[str] = mapped_column(String(100), nullable=False)
