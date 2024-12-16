from dataclasses import dataclass
from datetime import date

from infrastructure.clients.tinkoff.schemas import Item


@dataclass
class CreateInvoiceCommand:
    legal_entity_id: int
    amount: int
    json_meta_info: dict
    due_date: date
    invoice_date: date
    items: list[Item]
    phone: str
    comment: str


@dataclass
class UpdateInvoiceCommand:
    invoice_id: int
    update_data: dict[str, str | int]
