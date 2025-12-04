import sys
import os
import pytest
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy import text
from fastapi.testclient import TestClient # Import TestClient

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__))) # Add the backend directory to sys.path

# Import the Base from your database setup
from backend.src.db.database import Base, get_db
from backend.main import app # Import your FastAPI app instance

pytest_plugins = ["pytest_asyncio"]

# Define a test database URL for an in-memory SQLite database
TEST_SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

@pytest.fixture(scope="function")
async def db_session_fixture() -> AsyncSession:
    """
    Fixture that provides a fresh, independent database session for each test function.
    Rolls back transactions after each test.
    """
    test_engine = create_async_engine(TEST_SQLALCHEMY_DATABASE_URL, echo=False)
    TestingSessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=test_engine, class_=AsyncSession)

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all) # Create tables for models inheriting from Base
        async with TestingSessionLocal(bind=conn) as session:
            yield session
            await session.rollback() # Rollback all changes made during the test
    await test_engine.dispose() # Dispose of engine connections after test

@pytest.fixture(scope="function")
def test_app(db_session_fixture: AsyncSession):
    """
    Fixture that provides a TestClient with the overridden get_db dependency
    to use the test database session.
    """
    # This override will return the session directly, not yield it.
    # This deviates from the original get_db's generator pattern but tests if direct session works.
    async def get_db_override(): # This is a regular function, not async
        yield db_session_fixture # Yield the already resolved AsyncSession

    app.dependency_overrides[get_db] = get_db_override

    with TestClient(app) as client:
        yield client
    
    app.dependency_overrides.clear()