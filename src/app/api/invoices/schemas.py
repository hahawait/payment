import re
from datetime import date

from pydantic import BaseModel, Field, field_validator, model_validator

from infrastructure.clients.tinkoff.schemas import Item


class InvoiceDTO(BaseModel):
    id: int
    legal_entity_id: int
    amount: int
    status: str
    json_meta_info: dict


class CreateInvoiceDTO(BaseModel):
    legal_entity_id: int
    amount: int
    json_meta_info: dict
    due_date: date = Field(description="Срок оплаты. Должен быть не меньше даты выставления счета")
    invoice_date: date = Field(
        date.today(),
        description="Дата выставления счета. Если не указана, счет выставляется текущей датой"
    )
    items: list[Item]
    phone: str
    comment: str

    @model_validator(mode="before")
    @classmethod
    def date_validation(cls, fields) -> "CreateInvoiceDTO":
        if fields["due_date"] < fields["invoice_date"]:
            raise ValueError(
                "Срок оплаты. Должен быть не меньше даты выставления счета"
            )
        return fields

    @field_validator("phone")
    @classmethod
    def phone(cls, v: str) -> str:
        if not re.match(r"^\+7\d{10}$", v):
            raise ValueError("Номер мобильного телефона должен начинаться с +7 и содержать 10 цифр")
        return v


class UpdateInvoiceDTO(BaseModel):
    legal_entity_id: int | None = None
    amount: int | None = None
    json_meta_info: dict | None = None
