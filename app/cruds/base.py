from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete

from app.db.base_alembic import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**

        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    async def get_by_id(self, db: AsyncSession, *, id: int) -> Optional[ModelType]:
        q = select(self.model).filter(self.model.id == id)
        res = await db.execute(q)
        return res.scalar()

    async def get_first(self, db: AsyncSession) -> Optional[ModelType]:
        q = select(self.model)
        res = await db.execute(q)
        return res.scalar()

    async def get(self, db: AsyncSession, id: Any) -> Optional[ModelType]:
        q = select(self.model).filter(self.model.id == id)
        res = await db.execute(q)
        return res.scalar()

    async def get_all(
            self, db: AsyncSession) -> List[ModelType]:
        q = select(self.model)
        res = await db.execute(q)
        return res.scalars().all()

    async def create(self, db: AsyncSession, *, obj_in: CreateSchemaType) -> ModelType:
        db_obj = self.model(**obj_in.model_dump(exclude_unset=True))  # type: ignore
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def lock_row(self, db: AsyncSession, *, id: int) -> ModelType:
        q = select(self.model).filter(self.model.id == id).with_for_update()
        res = await db.execute(q)
        return res.scalar()

    async def update(
            self,
            db: AsyncSession,
            *,
            db_obj: ModelType = None,
            obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:

        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
        if not db_obj:
            db_obj = await self.get_by_id(db, id=obj_in.id)
        obj_data = jsonable_encoder(db_obj)

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def remove(self, db: AsyncSession, *, id: int) -> bool:
        q = delete(self.model).where(self.model.id == id)
        await db.execute(q)
        await db.commit()
        return True
