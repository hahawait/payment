from pydantic import BaseModel


class InvoiceInLegalEntity(BaseModel):
    id: int
    legal_entity_id: int
    amount: int
    status: str
    json_meta_info: dict


class LegalEntityDTO(BaseModel):
    id: int
    account_number: int
    sender_account_number: int
    payment_name: str
    payment_inn: int
    payment_kpp: int
    payment_email: str
    invoices: set[InvoiceInLegalEntity] | None = None


class CreateLegalEntityDTO(BaseModel):
    account_number: int
    sender_account_number: int
    payment_name: str
    payment_inn: int
    payment_kpp: int
    payment_email: str


class UpdateLegalEntityDTO(BaseModel):
    account_number: int | None = None
    sender_account_number: int | None = None
    payment_name: str | None = None
    payment_inn: int | None = None
    payment_kpp: int | None = None
    payment_email: str | None = None
