from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from config import settings

# Engine
engine = create_async_engine(
    settings.DATABASE_URL_asyncpg,
    echo=False,
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True,
)

# Session maker
async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)

# Dependency
async def get_session() -> AsyncSession: #type:ignore
    async with async_session_maker() as session:
        try:
            yield session #type:ignore
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()