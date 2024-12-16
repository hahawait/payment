from dataclasses import dataclass


@dataclass
class CreateLegalEntityCommand:
    account_number: int
    sender_account_number: int
    payment_name: str
    payment_inn: int
    payment_kpp: int
    payment_email: str


@dataclass
class UpdateLegalEntityCommand:
    legal_entity_id: int
    update_data: dict[str, str | int]
