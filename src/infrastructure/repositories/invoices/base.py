from abc import ABC, abstractmethod
from dataclasses import dataclass

from domain.entities.invoices import Invoice


@dataclass
class BaseInvoiceRepository(ABC):
    @abstractmethod
    async def create_invoice(self, invoice: Invoice) -> Invoice:
        raise NotImplementedError

    @abstractmethod
    async def get_invoice_by_id(self, invoice_id: int) -> Invoice | None:
        raise NotImplementedError

    @abstractmethod
    async def get_invoices(self) -> list[Invoice]:
        raise NotImplementedError

    @abstractmethod
    async def update_invoice(self, invoice: Invoice) -> Invoice:
        raise NotImplementedError

    @abstractmethod
    async def delete_invoice(self, invoice_id: int) -> Invoice | None:
        raise NotImplementedError
