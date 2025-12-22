from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from typing import AsyncGenerator
from backend.src.config.settings import settings


# Create async engine
engine = create_async_engine(
    settings.database_url,
    echo=settings.debug,  # Set to True to see SQL queries
    pool_pre_ping=True,  # Verify connections before use
)

# Create async session maker
async_session = sessionmaker(
    engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)

# Create base class for declarative models
Base = declarative_base()

# Create metadata instance
metadata = MetaData()


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency to get database session
    """
    async with async_session() as session:
        yield session
        await session.close()