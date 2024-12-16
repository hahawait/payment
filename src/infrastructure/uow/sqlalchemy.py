from dataclasses import dataclass
from types import TracebackType
from typing import Self

from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.repositories.invoices.sqlalchemy import SQLAlchemyInvoiceRepository
from infrastructure.repositories.legal_entities.sqlalchemy import SQLAlchemyLegalEntityRepository
from infrastructure.uow.base import BaseUnitOfWork


@dataclass
class SQLAlchemyUnitOfWork(BaseUnitOfWork):
    _session: AsyncSession = None

    async def __aenter__(self) -> Self:
        await self._session.begin()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        try:
            if exc_type is None:
                await self._session.commit()
            else:
                await self._session.rollback()
        finally:
            await self._session.close()

    def _session_check(self) -> None:
        if not self._session:
            raise ValueError("Session is not initialized")

    @property
    def invoices(self) -> SQLAlchemyInvoiceRepository:
        self._session_check()
        return SQLAlchemyInvoiceRepository(self._session)

    @property
    def legal_entities(self) -> SQLAlchemyLegalEntityRepository:
        self._session_check()
        return SQLAlchemyLegalEntityRepository(self._session)
