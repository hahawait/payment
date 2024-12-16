from dataclasses import dataclass

from logic.exceptions.base import LogicException


@dataclass(eq=False)
class LegalEntityNotFoundException(LogicException):
    legal_entity_id: int

    @property
    def status_code(self) -> int:
        return 404

    @property
    def message(self) -> str:
        return f"Юр.лицо с идентификатором {self.legal_entity_id} не найдено"
