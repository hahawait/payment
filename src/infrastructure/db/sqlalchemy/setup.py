from typing import AsyncContextManager, Callable

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from config import PGConfig


def create_engine(db: PGConfig, echo: bool = False) -> AsyncEngine:
    engine = create_async_engine(db.pg_database_url, echo=echo)
    return engine



def create_session_pool(
    engine: AsyncEngine,
) -> Callable[[], AsyncContextManager[AsyncSession]]:
    session_pool = sessionmaker(
        bind=engine, expire_on_commit=False, class_=AsyncSession
    )
    return session_pool
