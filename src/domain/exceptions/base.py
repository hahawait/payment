from dataclasses import dataclass


@dataclass(eq=False)
class ApplicationException(Exception):

    @property
    def status_code(self) -> int:
        return 400

    @property
    def message(self) -> str:
        return "Произошла ошибка приложения"
