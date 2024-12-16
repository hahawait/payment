from domain.entities.base import BaseEntity


class Invoice(BaseEntity):
    id: int | None = None
    legal_entity_id: int
    amount: int
    status: str
    json_meta_info: dict
