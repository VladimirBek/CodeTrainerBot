from typing import Optional

from pydantic import BaseModel


class LevelSchemaCreate(BaseModel):
    difficult: int


class LevelSchemaUpdate(BaseModel):
    difficult: Optional[int] = None
