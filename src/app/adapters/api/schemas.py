from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

from src.app.core.excetions import enums


class APIModel(BaseModel):
    model_config = ConfigDict(from_attributes=True, alias_generator=to_camel, populate_by_name=True)


class SimpleApiError(APIModel):
    success: bool
    code: enums.ErrorCodes
    message: str
