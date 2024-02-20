from typing import Optional

from pydantic import BaseModel


class CategorySchemaCreate(BaseModel):
    name: str


class CategorySchemaUpdate(BaseModel):
    name: Optional[str] = None
