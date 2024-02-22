from typing import Optional

from app.cruds.base import CRUDBase
from app.models import Level
from app.schemas import LevelSchemaCreate, LevelSchemaUpdate
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class CRUDLevel(CRUDBase[Level, LevelSchemaCreate, LevelSchemaUpdate]):

    async def get_by_level(self, db: AsyncSession, *, difficult: int) -> Optional[Level]:
        q = select(Level).filter(Level.difficult == difficult)
        res = await db.execute(q)
        return res.scalar()


crud_level = CRUDLevel(Level)
