from typing import Optional

from pydantic import BaseModel


class ExerciseSchemaCreate(BaseModel):
    cf_id: str
    url: str
    name: str
    topic: str
    count_solved: int
    difficult: int
    task: Optional[str] = None


class ExerciseSchemaUpdate(BaseModel):
    cf_id: Optional[str] = None
    url: Optional[str] = None
    name: Optional[str] = None
    topic: Optional[str] = None
    count_solved: Optional[int] = None
    difficult: Optional[int] = None
    task: Optional[str] = None

