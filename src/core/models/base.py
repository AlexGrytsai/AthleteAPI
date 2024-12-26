from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    declared_attr,
)


class Base(DeclarativeBase):
    """
    The base class for all database models.

    This class inherits from DeclarativeBase, which is the base class
    for all SQLAlchemy models.
    It provides a basic structure for defining database tables
    and relationships.
    """

    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}s"

    id: Mapped[int] = mapped_column(primary_key=True)
