from typing import Optional

from cruds.base import CRUDBase
from models.excercise import Exercise
from schemas import ExerciseSchemaUpdate, ExerciseSchemaCreate
from sqlalchemy import select, AsyncSession


class CRUDExercise(CRUDBase[Exercise, ExerciseSchemaCreate, ExerciseSchemaUpdate]):

    async def get_by_cf_id(self, db: AsyncSession, *, cf_id: str) -> Optional[Exercise]:
        q = select(Exercise).filter(Exercise.cf_id == cf_id)
        res = await db.execute(q)
        return res.scalar()


crud_exercise = CRUDExercise(Exercise)
