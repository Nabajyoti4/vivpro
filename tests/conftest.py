import asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, AsyncEngine
import pytest
from sqlmodel import SQLModel


from app.models.songs import Songs
from app.models.songs import ModeEnum
from decimal import Decimal


@pytest.fixture(scope="session")
def db_engine() -> AsyncEngine:
    return create_async_engine(
        "postgresql+asyncpg://postgres:nabapgadmin@localhost:5432/test_vivpro"
    )


# drop all database every time when test complete
@pytest.fixture(scope="session")
async def async_db_session(db_engine: AsyncEngine):
    async with db_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    yield db_engine

    async with db_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)


# truncate all table to isolate tests
@pytest.fixture(scope="function")
async def async_db(async_db_session):
    async with async_db_session.begin():
        yield async_db_session
        await async_db_session.rollback()


# let test session to know it is running inside event loop
@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


# assume we have a example model
@pytest.fixture
async def async_example_orm(async_db: AsyncSession) -> Songs:
    example = Songs(
        playlist_id="PL123456",
        title="Sample Song",
        danceability=Decimal("0.85"),
        energy=Decimal("0.75"),
        mode=ModeEnum.on,
        acousticness=Decimal("0.12"),
        tempo=Decimal("120.123"),
        duration_ms=240000,
        num_sections=10,
        num_segments=20,
        rating=5,
    )
    async_db.add(example)
    await async_db.commit()
    await async_db.refresh(example)
    return example
