from dataclasses import dataclass

from domain.entities.legal_entities import LegalEntity
from infrastructure.uow.sqlalchemy import SQLAlchemyUnitOfWork
from logic.commands.legal_entities import CreateLegalEntityCommand, UpdateLegalEntityCommand
from logic.exceptions.legal_entities import LegalEntityNotFoundException
from logic.usecases.base import BaseUseCase


@dataclass
class GetLegalEntitiesUseCase(BaseUseCase):
    uow: SQLAlchemyUnitOfWork

    async def execute(self) -> list[LegalEntity]:
        async with self.uow as uow:
            return await uow.legal_entities.get_legal_entities()


@dataclass
class GetLegalEntityByIdUseCase(BaseUseCase):
    uow: SQLAlchemyUnitOfWork

    async def execute(self, legal_entity_id: int) -> LegalEntity:
        async with self.uow as uow:
            legal_entity = await uow.legal_entities.get_legal_entity_by_id(legal_entity_id)
            if not legal_entity:
                raise LegalEntityNotFoundException(legal_entity_id)
            return legal_entity


@dataclass
class CreateLegalEntityUseCase(BaseUseCase):
    uow: SQLAlchemyUnitOfWork

    async def execute(self, create_command: CreateLegalEntityCommand) -> LegalEntity:
        async with self.uow as uow:
            legal_entity = LegalEntity(
                account_number=create_command.account_number,
                sender_account_number=create_command.sender_account_number,
                payment_name=create_command.payment_name,
                payment_inn=create_command.payment_inn,
                payment_kpp=create_command.payment_kpp,
                payment_email=create_command.payment_email,
            )
            created_legal_entity = await uow.legal_entities.create_legal_entity(legal_entity)
        return created_legal_entity


@dataclass
class UpdateLegalEntityUseCase(BaseUseCase):
    uow: SQLAlchemyUnitOfWork

    async def execute(self, update_command: UpdateLegalEntityCommand) -> LegalEntity:
        async with self.uow as uow:
            legal_entity = await uow.legal_entities.get_legal_entity_by_id(update_command.legal_entity_id)
            if not legal_entity:
                raise LegalEntityNotFoundException(update_command.legal_entity_id)
            for key, value in update_command.update_data.items():
                setattr(legal_entity, key, value)

            return await uow.legal_entities.update_legal_entity(legal_entity)


@dataclass
class DeleteLegalEntityUseCase(BaseUseCase):
    uow: SQLAlchemyUnitOfWork

    async def execute(self, legal_entity_id: int) -> LegalEntity:
        async with self.uow as uow:
            legal_entity = await uow.legal_entities.get_legal_entity_by_id(legal_entity_id)
            if not legal_entity:
                raise LegalEntityNotFoundException(legal_entity_id)
            await uow.legal_entities.delete_legal_entity(legal_entity_id)
            return legal_entity
