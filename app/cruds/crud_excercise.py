from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.cruds.base import CRUDBase
from app.models.excercise import Exercise
from app.schemas import ExerciseSchemaUpdate, ExerciseSchemaCreate


class CRUDExercise(CRUDBase[Exercise, ExerciseSchemaCreate, ExerciseSchemaUpdate]):

    async def get_by_cf_id(self, db: AsyncSession, *, cf_id: str) -> Optional[Exercise]:
        q = select(Exercise).filter(Exercise.cf_id == cf_id)
        res = await db.execute(q)
        return res.scalar()


crud_exercise = CRUDExercise(Exercise)
