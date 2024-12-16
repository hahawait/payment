from dataclasses import dataclass

from sqlalchemy import delete, select

from domain.entities.legal_entities import LegalEntity
from infrastructure.db.sqlalchemy.models import LegalEntityModel
from infrastructure.mappers.legal_entity import LegalEntityMapper
from infrastructure.repositories.base.base import BaseSQLAlchemyRepository
from infrastructure.repositories.legal_entities.base import BaseLegalEntityRepository


@dataclass
class SQLAlchemyLegalEntityRepository(BaseLegalEntityRepository, BaseSQLAlchemyRepository):
    model = LegalEntityModel

    async def create_legal_entity(self, legal_entity: LegalEntity) -> LegalEntity:
        instance = LegalEntityMapper.to_model(legal_entity)
        self.session.add(instance)
        await self.session.flush()
        return LegalEntityMapper.to_domain(instance)

    async def get_legal_entity_by_id(self, legal_entity_id: int) -> LegalEntity | None:
        query = select(self.model).where(self.model.id == legal_entity_id)
        result = await self.session.execute(query)
        model = result.scalar_one_or_none()
        if not model:
            return None
        return LegalEntityMapper.to_domain(model)

    async def get_legal_entities(self) -> list[LegalEntity]:
        query = select(self.model)
        result = await self.session.execute(query)
        return LegalEntityMapper.to_domain_from_models(result.scalars())

    async def update_legal_entity(self, legal_entity: LegalEntity) -> LegalEntity:
        instance = LegalEntityMapper.to_model(legal_entity)
        updated = await self.session.merge(instance)
        return LegalEntityMapper.to_domain(updated)

    async def delete_legal_entity(self, legal_entity_id: int) -> None:
        query = delete(self.model).where(self.model.id == legal_entity_id)
        await self.session.execute(query)
