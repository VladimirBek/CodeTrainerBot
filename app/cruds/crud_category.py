from typing import Optional, List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.cruds.base import CRUDBase
from app.models import Exercise
from app.models.category import Category
from app.schemas.category_schema import CategorySchemaCreate, CategorySchemaUpdate


class CRUDCategory(CRUDBase[Category, CategorySchemaCreate, CategorySchemaUpdate]):

    async def get_by_name(self, db: AsyncSession, *, name: str) -> Optional[Category]:
        q = select(Category).filter(Category.name == name)
        res = await db.execute(q)
        return res.scalar()


crud_category = CRUDCategory(Category)
