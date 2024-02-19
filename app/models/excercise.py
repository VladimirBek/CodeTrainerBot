from db.base_class import Base
from models.basemodel import ModelBase
from sqlalchemy import Column
from sqlalchemy.types import Integer, Text


class Exercise(Base, ModelBase):
    id = Column(Integer, primary_key=True, autoincrement=True)
    cf_id = Column(Text, nullable=False)
    url = Column(Text, nullable=False)
    name = Column(Text, nullable=False)
    topic = Column(Text, nullable=False)
    count_solved = Column(Integer, server_default="0", nullable=False)
    difficult = Column(Integer, server_default="0", nullable=False)
    task = Column(Text)



