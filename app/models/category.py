from db.base_class import Base
from models.basemodel import ModelBase
from sqlalchemy import Column
from sqlalchemy.types import Integer, Text


class Category(Base, ModelBase):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text)
