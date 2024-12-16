from dishka import Provider, Scope, provide

from infrastructure.uow.sqlalchemy import SQLAlchemyUnitOfWork
from logic.usecases.legal_entities import (
    CreateLegalEntityUseCase, GetLegalEntitiesUseCase, GetLegalEntityByIdUseCase,
    UpdateLegalEntityUseCase, DeleteLegalEntityUseCase
)


class LegalEntitiesProvider(Provider):
    scope = Scope.REQUEST

    @provide
    def create_legal_entity(self, uow: SQLAlchemyUnitOfWork) -> CreateLegalEntityUseCase:
        return CreateLegalEntityUseCase(uow=uow)

    @provide
    def get_legal_entities(self, uow: SQLAlchemyUnitOfWork) -> GetLegalEntitiesUseCase:
        return GetLegalEntitiesUseCase(uow=uow)

    @provide
    def get_legal_entity_by_id(self, uow: SQLAlchemyUnitOfWork) -> GetLegalEntityByIdUseCase:
        return GetLegalEntityByIdUseCase(uow=uow)

    @provide
    def update_legal_entity(self, uow: SQLAlchemyUnitOfWork) -> UpdateLegalEntityUseCase:
        return UpdateLegalEntityUseCase(uow=uow)

    @provide
    def delete_legal_entity(self, uow: SQLAlchemyUnitOfWork) -> DeleteLegalEntityUseCase:
        return DeleteLegalEntityUseCase(uow=uow)
