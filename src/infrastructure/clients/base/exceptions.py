from dataclasses import dataclass

from domain.exceptions.base import ApplicationException


@dataclass(eq=False)
class ClientException(ApplicationException):
    @property
    def status_code(self) -> int:
        return 400

    @property
    def message(self) -> str:
        return "Произошла ошибка клиента"
