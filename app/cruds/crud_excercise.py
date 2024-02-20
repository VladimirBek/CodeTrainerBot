from typing import Optional, Sequence

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

    async def get_by_category_id(self, db: AsyncSession, *, topic_id: int) -> Optional[Sequence[Exercise]]:
        q = select(Exercise).filter(Exercise.topic_id == topic_id)
        res = await db.execute(q)
        return res.scalars().all()
    async def get_by_difficulty(self, db: AsyncSession, *, difficult: int) -> Optional[Sequence[Exercise]]:
        q = select(Exercise).filter(Exercise.difficult == difficult)
        res = await db.execute(q)
        return res.scalars().all()

    async def get_by_difficulty_and_topic(self, db: AsyncSession, *, difficulty: int, topic_id: int) -> Optional[Sequence[Exercise]]:
        q = select(Exercise).filter(Exercise.difficult == difficulty, Exercise.topic_id == topic_id)
        res = await db.execute(q)
        return res.scalars().all()

crud_exercise = CRUDExercise(Exercise)
