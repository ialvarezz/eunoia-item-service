from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os

load_dotenv()

# Load the DATABASE_URL from the environment variables
DATABASE_URL = os.getenv("DATABASE_URL")

# Create an async engine with the database URL
engine = create_async_engine(DATABASE_URL, echo=True)

# Create a sessionmaker that will use the async engine
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autoflush=False,
    autocommit=False
)

# Define a base class for all models to inherit from
Base = declarative_base()

# Dependency to get the session
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except:
            await session.rollback()
            raise
        finally:
            await session.close()

