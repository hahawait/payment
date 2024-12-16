from typing import Any

from pydantic import BaseModel, ConfigDict


class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class APIResponse(BaseSchema):
    status: int
    result: dict[Any, Any] | list[dict[Any, Any]] | None
