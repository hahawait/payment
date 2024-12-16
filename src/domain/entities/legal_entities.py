from domain.entities.base import BaseEntity
from domain.entities.invoices import Invoice


class LegalEntity(BaseEntity):
    id: int | None = None
    account_number: int
    sender_account_number: int
    payment_name: str
    payment_inn: int
    payment_kpp: int
    payment_email: str
    invoices: set[int | Invoice] = set()
