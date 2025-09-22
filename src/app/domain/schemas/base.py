from datetime import datetime
from typing import Any
import uuid

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class BaseSchema(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        alias_generator=to_camel,
        populate_by_name=True,
    )

    def __init__(self, **data: Any) -> None:
        for field, value in data.items():
            if isinstance(value, BaseModel):
                data[field] = value.model_dump(exclude_unset=True)

        super().__init__(**data)


class BaseModelSchema(BaseSchema):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
