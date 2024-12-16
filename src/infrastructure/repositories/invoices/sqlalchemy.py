from dataclasses import dataclass

from sqlalchemy import delete, select

from domain.entities.invoices import Invoice
from infrastructure.db.sqlalchemy.models import InvoiceModel
from infrastructure.mappers.invoices import InvoiceMapper
from infrastructure.repositories.base.base import BaseSQLAlchemyRepository
from infrastructure.repositories.invoices.base import BaseInvoiceRepository


@dataclass
class SQLAlchemyInvoiceRepository(BaseInvoiceRepository, BaseSQLAlchemyRepository):
    model = InvoiceModel

    async def create_invoice(self, invoice: Invoice) -> Invoice:
        instance = InvoiceMapper.to_model(invoice)
        self.session.add(instance)
        await self.session.flush()
        return InvoiceMapper.to_domain(instance)

    async def get_invoice_by_id(self, invoice_id: int) -> Invoice | None:
        query = select(self.model).where(self.model.id == invoice_id)
        result = await self.session.execute(query)
        model = result.scalar_one_or_none()
        if not model:
            return None
        return InvoiceMapper.to_domain(model)

    async def get_invoices(self) -> list[Invoice]:
        query = select(self.model)
        result = await self.session.execute(query)
        return InvoiceMapper.to_domain_from_models(result.scalars())

    async def update_invoice(self, invoice: Invoice) -> Invoice:
        instance = InvoiceMapper.to_model(invoice)
        updated = await self.session.merge(instance)
        return InvoiceMapper.to_domain(updated)

    async def delete_invoice(self, invoice_id: int) -> None:
        query = delete(self.model).where(self.model.id == invoice_id)
        await self.session.execute(query)
