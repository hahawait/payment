from domain.entities.legal_entities import LegalEntity
from infrastructure.db.sqlalchemy.models import LegalEntityModel
from infrastructure.mappers.base import BaseMapper
from infrastructure.mappers.invoices import InvoiceMapper


class LegalEntityMapper(BaseMapper[LegalEntityModel, LegalEntity]):
    @classmethod
    def to_model(cls, domain: LegalEntity) -> LegalEntityModel:
        return LegalEntityModel(
            id=domain.id,
            account_number=domain.account_number,
            sender_account_number=domain.sender_account_number,
            payment_name=domain.payment_name,
            payment_inn=domain.payment_inn,
            payment_kpp=domain.payment_kpp,
            payment_email=domain.payment_email,
            invoices={InvoiceMapper.to_model(invoice) for invoice in domain.invoices}
        )

    @classmethod
    def to_domain(cls, model: LegalEntityModel) -> LegalEntity:
        return LegalEntity(
            id=model.id,
            account_number=model.account_number,
            sender_account_number=model.sender_account_number,
            payment_name=model.payment_name,
            payment_inn=model.payment_inn,
            payment_kpp=model.payment_kpp,
            payment_email=model.payment_email,
            invoices={InvoiceMapper.to_domain(invoice) for invoice in model.invoices}
        )
