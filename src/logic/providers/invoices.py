from dishka import Provider, Scope, provide

from infrastructure.uow.sqlalchemy import SQLAlchemyUnitOfWork
from logic.usecases.invoices import (
    CreateInvoiceUseCase, GetInvoicesUseCase, GetInvoiceByIdUseCase,
    UpdateInvoiceUseCase, DeleteInvoiceUseCase
)


class InvoicesProvider(Provider):
    scope = Scope.REQUEST

    @provide
    def create_invoice(self, uow: SQLAlchemyUnitOfWork) -> CreateInvoiceUseCase:
        return CreateInvoiceUseCase(uow=uow)

    @provide
    def get_invoices(self, uow: SQLAlchemyUnitOfWork) -> GetInvoicesUseCase:
        return GetInvoicesUseCase(uow=uow)

    @provide
    def get_invoice_by_id(self, uow: SQLAlchemyUnitOfWork) -> GetInvoiceByIdUseCase:
        return GetInvoiceByIdUseCase(uow=uow)

    @provide
    def update_invoice(self, uow: SQLAlchemyUnitOfWork) -> UpdateInvoiceUseCase:
        return UpdateInvoiceUseCase(uow=uow)

    @provide
    def delete_invoice(self, uow: SQLAlchemyUnitOfWork) -> DeleteInvoiceUseCase:
        return DeleteInvoiceUseCase(uow=uow)
