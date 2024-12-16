from abc import ABC, abstractmethod
from dataclasses import dataclass

from domain.entities.legal_entities import LegalEntity


@dataclass
class BaseLegalEntityRepository(ABC):
    @abstractmethod
    async def create_legal_entity(self, legal_entity: LegalEntity) -> LegalEntity:
        raise NotImplementedError

    @abstractmethod
    async def get_legal_entity_by_id(self, legal_entity_id: int) -> LegalEntity | None:
        raise NotImplementedError

    @abstractmethod
    async def get_legal_entities(self) -> list[LegalEntity]:
        raise NotImplementedError

    @abstractmethod
    async def update_legal_entity(self, legal_entity: LegalEntity) -> LegalEntity:
        raise NotImplementedError

    @abstractmethod
    async def delete_legal_entity(self, legal_entity_id: int) -> LegalEntity | None:
        raise NotImplementedError
