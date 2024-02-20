from sqlalchemy import Column
from sqlalchemy.types import Integer

from app.db.base_alembic import Base
from app.models.basemodel import ModelBase


class Level(Base, ModelBase):
    id = Column(Integer, primary_key=True, autoincrement=True)
    difficult = Column(Integer, nullable=True)
