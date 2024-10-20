from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.config import settings

from sqlalchemy.orm import sessionmaker


DATABASE_URL = str(settings.SQLALCHEMY_DATABASE_URI)

async_engine = create_async_engine(DATABASE_URL, echo=True, future=True)


async def get_async_session() -> AsyncSession:
    async_session = sessionmaker(
        bind=async_engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session
