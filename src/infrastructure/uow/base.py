from abc import ABC, abstractmethod
from dataclasses import dataclass
from types import TracebackType

from infrastructure.repositories.invoices.base import BaseInvoiceRepository
from infrastructure.repositories.legal_entities.base import BaseLegalEntityRepository


@dataclass
class BaseUnitOfWork(ABC):

    @abstractmethod
    async def __aenter__(self) -> "BaseUnitOfWork": ...

    @abstractmethod
    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None: ...

    @property
    def invoices(self) -> BaseInvoiceRepository:
        return BaseInvoiceRepository()

    @property
    def legal_entities(self) -> BaseLegalEntityRepository:
        return BaseLegalEntityRepository()
