from abc import ABC
from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession


@dataclass
class BaseSQLAlchemyRepository(ABC):
    model = None
    session: AsyncSession
