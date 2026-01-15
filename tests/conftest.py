import pytest_asyncio
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from config import settings as s
from db.models import Base, VideosOrm
from schemas.videos import VideoAddForm
from random import randint, choice
from datetime import datetime, timedelta


@pytest_asyncio.fixture(scope="function")
async def db_engine():
    """Engine на всю сессию"""
    engine = create_async_engine(
        url=s.DATABASE_URL_asyncpg,
        echo=False
    )
    yield engine
    await engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def db_tables(db_engine: AsyncEngine):
    """Таблицы для каждого теста"""
    async with db_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    yield
    
    async with db_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture(scope="function")
async def db_session(db_engine: AsyncEngine, db_tables):
    """Новая сессия для каждого теста"""
    async_session_maker = async_sessionmaker(
        bind=db_engine,
        class_=AsyncSession,
        expire_on_commit=False
    )
    
    async with async_session_maker() as session:
        yield session


@pytest_asyncio.fixture(scope="function")
async def video_notes(db_session: AsyncSession):
    for _ in range(100):
        video = VideoAddForm(
            video_path=f"test_{randint(10, 10_000)}",
            start_time=datetime.now() + timedelta(minutes=randint(1, 10_000)),
            duration=timedelta(minutes=randint(1, 15)),
            camera_number=randint(1, 10),
            location=choice(["yard", "street", "inside"])
        )
        video_orm = VideosOrm(**video.model_dump())
        db_session.add(video_orm)
        await db_session.commit()
        await db_session.refresh(video_orm)


@pytest_asyncio.fixture(scope="function")
async def video_note(db_session: AsyncSession):
    video = VideoAddForm(
        video_path=f"test_{randint(10, 10_000)}",
        start_time=datetime.now() + timedelta(minutes=randint(1, 10_000)),
        duration=timedelta(minutes=randint(1, 15)),
        camera_number=randint(1, 10),
        location=choice(["yard", "street", "inside"])
    )
    video_orm = VideosOrm(**video.model_dump())
    db_session.add(video_orm)
    await db_session.commit()
    await db_session.refresh(video_orm)
    