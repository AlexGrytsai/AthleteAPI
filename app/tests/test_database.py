import unittest

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
)

from app.core.database import create_database_engine, create_session_factory


class TestDatabaseFunctions(unittest.IsolatedAsyncioTestCase):
    async def test_create_database_engine(self):
        database_url = "sqlite+aiosqlite:///:memory:"
        engine = create_database_engine(database_url)

        self.assertIsInstance(engine, AsyncEngine)
        self.assertEqual(str(engine.url), database_url)

        await engine.dispose()

    async def test_create_session_factory(self):
        database_url = "sqlite+aiosqlite:///:memory:"
        engine = create_database_engine(database_url)
        session_factory = create_session_factory(engine)

        self.assertIsInstance(session_factory, async_sessionmaker)
        self.assertTrue(issubclass(session_factory.class_, AsyncSession))

        await engine.dispose()
