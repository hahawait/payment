from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from domain.entities.base import BaseEntity
from infrastructure.db.sqlalchemy.models import BaseModel

M = TypeVar("M", bound=BaseModel)
D = TypeVar("D", bound=BaseEntity)


class BaseMapper(ABC, Generic[M, D]):

    @classmethod
    @abstractmethod
    def to_domain(cls, model: M) -> D:
        pass

    @classmethod
    @abstractmethod
    def to_model(cls, domain: D) -> M:
        pass

    @classmethod
    def to_domain_from_models(cls, models: list[M]) -> list[D]:
        return [cls.to_domain(model) for model in models]

    @classmethod
    def to_model_from_domains(cls, domains: list[D]) -> list[M]:
        return [cls.to_model(domain) for domain in domains]
