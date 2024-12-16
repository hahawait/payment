import re
from datetime import date
from typing import Literal
from uuid import UUID

from pydantic import Field, field_validator, model_validator

from infrastructure.clients.base.schemas import BaseSchema


class Payer(BaseSchema):
    name: str = Field(description="Наименование")
    inn: str = Field(description="Наименование плательщика")
    kpp: str = Field(description="КПП плательщика")

    @field_validator("name")
    @classmethod
    def name(cls, v: str) -> str:
        if len(v) > 512:
            raise ValueError("Наименование не может превышать 512 символов")
        return v

    @field_validator("inn")
    @classmethod
    def inn(cls, v: str) -> str:
        if len(v) not in [10, 12]:
            raise ValueError("ИНН должен содержать 10 или 12 цифр")
        return v

    @field_validator("kpp")
    @classmethod
    def kpp(cls, v: str) -> str:
        if len(v) != 9:
            raise ValueError("КПП должен содержать 9 цифр")
        return v


class Item(BaseSchema):
    name: str = Field(description="Наименование")
    price: int = Field(description="Цена за единицу в рублях")
    unit: str = Field(description="Единицы измерения")
    vat: Literal[None, 0, 10, 18, 20] = Field(description="НДС. None — без НДС")
    amount: int = Field(description="Количество единиц")


class SendInvoiceSchema(BaseSchema):
    invoice_number: str = Field(description="Номер счета", serialization_alias="invoiceNumber")
    due_date: date = Field(
        description="Срок оплаты. Должен быть не меньше даты выставления счета",
        serialization_alias="dueDate",
    )
    invoice_date: date = Field(
        default=date.today(),
        description="Дата выставления счета. Если не указана, счет выставляется текущей датой",
        serialization_alias="invoiceDate",
    )
    account_number: str = Field(
        description="Рублевый расчетный счет отправителя",
        serialization_alias="accountNumber",
    )
    payer: Payer = Field(description="Информация о плательщике")
    items: list[Item] = Field(description="Позиции счета")
    contacts: dict[str, str] = Field(description="Контакты для получения счета")
    contact_phone: str = Field(
        description="Номер мобильного телефона, на который придет СМС-сообщение со счетом",
        serialization_alias="contactPhone",
    )
    comment: str = Field(description="Комментарий")

    @model_validator(mode="before")
    @classmethod
    def date_validation(cls, fields) -> "SendInvoiceSchema":
        if fields["due_date"] < fields["invoice_date"]:
            raise ValueError(
                "Срок оплаты. Должен быть не меньше даты выставления счета"
            )
        return fields

    @field_validator('invoice_number')
    @classmethod
    def invoice_number(cls, v: str) -> str:
        if not re.match(r'^\d{1,15}$', v):
            raise ValueError('Номер счета должен содержать от 1 до 15 цифр')
        return v

    @field_validator('account_number')
    def account_number(cls, v: str) -> str:
        if not re.match(r'^\d{20}$|^\d{22}$', v):
            raise ValueError('Номер расчетного счета должен быть длиной 20 или 22 цифры')
        return v

    @field_validator("contact_phone")
    @classmethod
    def contact_phone(cls, v: str) -> str:
        if not re.match(r"^\+7\d{10}$", v):
            raise ValueError("Номер мобильного телефона должен начинаться с +7 и содержать 10 цифр")
        return v


class SendInvoiceResponse(BaseSchema):
    pdf_url: str = Field(
        description="Ссылка на PDF выставленного счета. Действительна в течение 10 дней",
        validation_alias="pdfUrl"
    )
    invoice_id: UUID = Field(
        description="Идентификатор выставленного счета",
        validation_alias="invoiceId"
    )
