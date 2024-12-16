from dataclasses import dataclass

from domain.entities.invoices import Invoice
from infrastructure.clients.tinkoff.client import TinkoffCli
from infrastructure.clients.tinkoff.schemas import Item, Payer, SendInvoiceSchema
from infrastructure.uow.sqlalchemy import SQLAlchemyUnitOfWork
from logic.commands.invoices import CreateInvoiceCommand, UpdateInvoiceCommand
from logic.exceptions.invoices import InvoiceNotFoundException
from logic.usecases.base import BaseUseCase


@dataclass
class GetInvoicesUseCase(BaseUseCase):
    uow: SQLAlchemyUnitOfWork

    async def execute(self) -> list[Invoice]:
        async with self.uow as uow:
            return await uow.invoices.get_invoices()


@dataclass
class GetInvoiceByIdUseCase(BaseUseCase):
    uow: SQLAlchemyUnitOfWork

    async def execute(self, invoice_id: int) -> Invoice:
        async with self.uow as uow:
            invoice = await uow.invoices.get_invoice_by_id(invoice_id)
            if not invoice:
                raise InvoiceNotFoundException(invoice_id)
            return invoice


@dataclass
class CreateInvoiceUseCase(BaseUseCase):
    uow: SQLAlchemyUnitOfWork
    tinkoff_cli: TinkoffCli

    async def execute(self, create_command: CreateInvoiceCommand) -> Invoice:
        cli: TinkoffCli = self.tinkoff_cli

        async with self.uow as uow:
            legal_entity = await uow.legal_entities.get_legal_entity_by_id(create_command.legal_entity_id)

            async with cli as cli:
                invoice_responce = await cli.send_invoice(
                    SendInvoiceSchema(
                        invoice_number=legal_entity.account_number,
                        due_date=create_command.due_date,
                        invoice_date=create_command.invoice_date,
                        account_number=legal_entity.sender_account_number,
                        payer=Payer(
                            name=legal_entity.payment_name,
                            inn=legal_entity.payment_inn,
                            kpp=legal_entity.payment_kpp,
                        ),
                        items=create_command.items,
                        contacts={"email": legal_entity.payment_email},
                        contact_phone=create_command.phone,
                        comment=create_command.comment,
                    )
                )
            invoice = Invoice(
                legal_entity_id=create_command.legal_entity_id,
                amount=create_command.amount,
                status=create_command.status,
                json_meta_info=create_command.json_meta_info
            )
            created_invoice = await uow.invoices.create_invoice(invoice)
        return created_invoice


@dataclass
class UpdateInvoiceUseCase(BaseUseCase):
    uow: SQLAlchemyUnitOfWork

    async def execute(self, update_command: UpdateInvoiceCommand) -> Invoice:
        async with self.uow as uow:
            invoice = await uow.invoices.get_invoice_by_id(update_command.invoice_id)
            if not invoice:
                raise InvoiceNotFoundException(update_command.invoice_id)
            for key, value in update_command.update_data.items():
                setattr(invoice, key, value)

            return await uow.invoices.update_invoice(invoice)


@dataclass
class DeleteInvoiceUseCase(BaseUseCase):
    uow: SQLAlchemyUnitOfWork

    async def execute(self, invoice_id: int) -> Invoice:
        async with self.uow as uow:
            invoice = await uow.invoices.get_invoice_by_id(invoice_id)
            if not invoice:
                raise InvoiceNotFoundException(invoice_id)
            await uow.invoices.delete_invoice(invoice_id)
            return invoice
