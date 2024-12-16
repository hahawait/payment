from domain.entities.invoices import Invoice
from infrastructure.db.sqlalchemy.models import InvoiceModel
from infrastructure.mappers.base import BaseMapper


class InvoiceMapper(BaseMapper[InvoiceModel, Invoice]):
    @classmethod
    def to_model(cls, domain: Invoice) -> InvoiceModel:
        return InvoiceModel(
            id=domain.id,
            legal_entity_id=domain.legal_entity_id,
            amount=domain.amount,
            status=domain.status,
            json_meta_info=domain.json_meta_info,
            created_at=domain.created_at,
            updated_at=domain.updated_at,
        )

    @classmethod
    def to_domain(cls, model: InvoiceModel) -> Invoice:
        return Invoice(
            id=model.id,
            legal_entity_id=model.legal_entity_id,
            amount=model.amount,
            status=model.status,
            json_meta_info=model.json_meta_info,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
