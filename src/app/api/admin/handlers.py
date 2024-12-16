from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, Depends, HTTPException, status

from app.api.admin.dependencies import verify_superadmin
from app.api.schemas import ErrorSchema
from app.api.invoices.schemas import CreateInvoiceDTO, InvoiceDTO, UpdateInvoiceDTO
from app.api.legal_entities.schemas import CreateLegalEntityDTO, LegalEntityDTO, UpdateLegalEntityDTO
from domain.exceptions.base import ApplicationException
from logic.commands.invoices import CreateInvoiceCommand, UpdateInvoiceCommand
from logic.commands.legal_entities import CreateLegalEntityCommand, UpdateLegalEntityCommand
from logic.usecases.invoices import (
    CreateInvoiceUseCase, DeleteInvoiceUseCase, GetInvoiceByIdUseCase,
    GetInvoicesUseCase, UpdateInvoiceUseCase
)
from logic.usecases.legal_entities import (
    CreateLegalEntityUseCase, DeleteLegalEntityUseCase, GetLegalEntityByIdUseCase,
    GetLegalEntitiesUseCase, UpdateLegalEntityUseCase
)

router = APIRouter(
    prefix="/admin",
    tags=["Админка"],
    dependencies=[Depends(verify_superadmin)],
    responses={
        401: {"description": "Unauthorized", "model": ErrorSchema}
    }
)


@router.get("/legal_entity")
@inject
async def get_legal_entities(
    use_case: FromDishka[GetLegalEntitiesUseCase],
) -> list[LegalEntityDTO]:
    """
    Получение списка юридических лиц
    """
    try:
        legal_entities = await use_case.execute()
    except ApplicationException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    return legal_entities


@router.get(
    "/legal_entity/{legal_entity_id}",
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "LegalEntity not found", "model": ErrorSchema}
    }
)
@inject
async def get_legal_entity(
    legal_entity_id: int,
    use_case: FromDishka[GetLegalEntityByIdUseCase],
) -> LegalEntityDTO:
    """
    Получение юридического лица по id
    """
    try:
        legal_entity = await use_case.execute(legal_entity_id=legal_entity_id)
    except ApplicationException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    return legal_entity


@router.post(
    "/legal_entity",
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_400_BAD_REQUEST: {"description": "Bad request", "model": ErrorSchema}
    }
)
@inject
async def create_legal_entity(
    legal_entity: CreateLegalEntityDTO,
    use_case: FromDishka[CreateLegalEntityUseCase],
) -> LegalEntityDTO:
    """
    Создание юридического лица
    """
    try:
        create_command = CreateLegalEntityCommand(**legal_entity.model_dump())
        created_legal_entity = await use_case.execute(create_command=create_command)
    except ApplicationException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    return created_legal_entity


@router.patch(
    "/legal_entity/{legal_entity_id}",
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "LegalEntity not found", "model": ErrorSchema},
        status.HTTP_400_BAD_REQUEST: {"description": "Bad request", "model": ErrorSchema}
    }
)
@inject
async def update_legal_entity(
    legal_entity_id: int,
    update_data: UpdateLegalEntityDTO,
    use_case: FromDishka[UpdateLegalEntityUseCase],
) -> LegalEntityDTO:
    """
    Обновление юридического лица по id
    """
    try:
        update_command = UpdateLegalEntityCommand(
            legal_entity_id=legal_entity_id,
            update_data=update_data.model_dump(exclude_none=True)
        )
        updated_legal_entity = await use_case.execute(update_command=update_command)
    except ApplicationException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    return updated_legal_entity


@router.delete(
    "/legal_entity/{legal_entity_id}",
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "LegalEntity not found", "model": ErrorSchema}
    }
)
@inject
async def delete_legal_entity(
    legal_entity_id: int,
    use_case: FromDishka[DeleteLegalEntityUseCase],
) -> LegalEntityDTO:
    """
    Удаление юридического лица по id
    """
    try:
        deleted_legal_entity = await use_case.execute(legal_entity_id=legal_entity_id)
    except ApplicationException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    return deleted_legal_entity


@router.get("/invoces")
@inject
async def get_invoices(
    use_case: FromDishka[GetInvoicesUseCase],
) -> list[InvoiceDTO]:
    """
    Получение списка счетов
    """
    try:
        invoices = await use_case.execute()
    except ApplicationException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    return invoices


@router.get(
    "/invoces/{invoice_id}",
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "Invoice not found", "model": ErrorSchema}
    }
)
@inject
async def get_invoice(
    invoice_id: int,
    use_case: FromDishka[GetInvoiceByIdUseCase],
) -> InvoiceDTO:
    """
    Получение счета по id
    """
    try:
        Invoice = await use_case.execute(invoice_id=invoice_id)
    except ApplicationException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    return Invoice


@router.post(
    "/invoces",
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_400_BAD_REQUEST: {"description": "Bad request", "model": ErrorSchema}
    }
)
@inject
async def create_invoice(
    invoice: CreateInvoiceDTO,
    use_case: FromDishka[CreateInvoiceUseCase],
) -> InvoiceDTO:
    """
    Создание счета
    """

    try:
        create_command = CreateInvoiceCommand(**invoice.model_dump())
        created_invoice = await use_case.execute(create_command=create_command)
    except ApplicationException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    return created_invoice


@router.patch(
    "/invoces/{invoice_id}",
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "Invoice not found", "model": ErrorSchema},
        status.HTTP_400_BAD_REQUEST: {"description": "Bad request", "model": ErrorSchema}
    }
)
@inject
async def update_invoice(
    invoice_id: int,
    update_data: UpdateInvoiceDTO,
    use_case: FromDishka[UpdateInvoiceUseCase],
) -> InvoiceDTO:
    """
    Обновление счета по id
    """
    try:
        update_command = UpdateInvoiceCommand(
            invoice_id=invoice_id,
            update_data=update_data.model_dump(exclude_none=True)
        )
        updated_invoice = await use_case.execute(update_command=update_command)
    except ApplicationException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    return updated_invoice


@router.delete(
    "/invoices/{invoice_id}",
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "Invoice not found", "model": ErrorSchema}
    }
)
@inject
async def delete_invoice(
    invoice_id: int,
    use_case: FromDishka[DeleteInvoiceUseCase],
) -> InvoiceDTO:
    """
    Удаление счета по id
    """
    try:
        deleted_invoice = await use_case.execute(invoice_id=invoice_id)
    except ApplicationException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    return deleted_invoice
