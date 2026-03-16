from typing import Generic, List, TypeVar

from pydantic import BaseModel, Field
from pydantic.generics import GenericModel

T = TypeVar("T")


class PaginationParams(BaseModel):
    limit: int = Field(20, ge=1, le=100, description="Number of items to return")
    offset: int = Field(0, ge=0, description="Number of items to skip")


class PaginatedResponse(GenericModel, Generic[T]):
    items: List[T]
    total: int = Field(..., description="Total number of records")
    limit: int = Field(..., description="Number of items returned")
    offset: int = Field(..., description="Number of items skipped")

    class Config:
        orm_mode = True
