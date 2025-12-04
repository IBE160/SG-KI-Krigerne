from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession, AsyncEngine
from sqlalchemy.orm import declarative_base
import os

from backend.src.db.__init__ import Base # Import Base from __init__.py

# Global variables for engine and sessionmaker, to be initialized once
_engine: AsyncEngine | None = None
_SessionLocal: type[AsyncSession] | None = None

def init_db_connection(database_url: str | None = None):
    """Initializes the database engine and sessionmaker.
    This function should be called once at application startup.
    Can be called with a specific database_url for testing/overrides.
    """
    global _engine, _SessionLocal

    # Only re-initialize if not already initialized with a different URL,
    # or if a new URL is explicitly provided to force re-initialization.
    current_db_url = _engine.url.__str__() if _engine else None if _engine else None

    if _engine is None or (database_url is not None and database_url != current_db_url):
        if database_url is None:
            database_url = os.getenv("DATABASE_URL", "postgresql+asyncpg://user:password@localhost/dbname")
        
        if _engine is not None:
            _engine.sync_engine.dispose()

        _engine = create_async_engine(database_url, echo=True)
        _SessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=_engine, class_=AsyncSession)
    
    return _engine, _SessionLocal

def get_engine() -> AsyncEngine:
    """Returns the initialized database engine."""
    global _engine, _SessionLocal
    if _engine is None:
        init_db_connection() # Lazy initialize if not already
    return _engine

def get_session_local() -> type[AsyncSession]:
    """Returns the initialized session local factory."""
    global _engine, _SessionLocal
    if _SessionLocal is None:
        init_db_connection() # Lazy initialize if not already
    return _SessionLocal

async def get_db():
    """Dependency to get a database session."""
    _SessionLocal = get_session_local() # Ensure SessionLocal is initialized
    async with _SessionLocal() as session:
        yield session

# Removed module-level call to init_db_connection()
# It should be explicitly called by main.py or test setup
