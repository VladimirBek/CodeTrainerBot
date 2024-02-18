from typing import Optional

from cruds.base import CRUDBase
from models.excercise import Exercise
from schemas import ExerciseSchemaUpdate, ExerciseSchemaCreate
from sqlalchemy import select, AsyncSession


class CRUDExercise(CRUDBase[Exercise, ExerciseSchemaCreate, ExerciseSchemaUpdate]):

    async def get_by_id(self, db: AsyncSession, *, id: int) -> Optional[Exercise]:
        q = select(Exercise).filter(Exercise.id == id)
        res = await db.execute(q)
        return res.scalar()


crud_exercise = CRUDExercise(Exercise)
