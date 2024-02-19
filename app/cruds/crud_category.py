from typing import Optional

from cruds.base import CRUDBase
from models.category import Category
from schemas.category_schema import CategorySchemaCreate, CategorySchemaUpdate
from sqlalchemy import select, AsyncSession


class CRUDCategory(CRUDBase[Category, CategorySchemaCreate, CategorySchemaUpdate]):

    async def get_by_name(self, db: AsyncSession, *, name: str) -> Optional[Category]:
        q = select(Category).filter(Category.name == name)
        res = await db.execute(q)
        return res.scalar()

crud_category = CRUDCategory(Category)