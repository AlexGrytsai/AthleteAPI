from app.core.config import settings
from app.core.database import create_database_engine, create_session_factory

engine = create_database_engine(settings.database_url)
session_factory = create_session_factory(engine)
