from dataclasses import dataclass

from logic.exceptions.base import LogicException


@dataclass(eq=False)
class InvoiceNotFoundException(LogicException):
    invoice_id: int

    @property
    def status_code(self) -> int:
        return 404

    @property
    def message(self) -> str:
        return f"Счет с идентификатором {self.invoice_id} не найден"
