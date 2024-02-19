from app.db.base_alembic import Base
from app.models.basemodel import ModelBase
from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import Integer, Text


class Exercise(Base, ModelBase):
    id = Column(Integer, primary_key=True, autoincrement=True)
    cf_id = Column(Text, nullable=False)
    url = Column(Text, nullable=False)
    name = Column(Text, nullable=False)
    topic_id = Column(Integer, ForeignKey("category.id"), nullable=False, index=True)
    count_solved = Column(Integer, server_default="0", nullable=False)
    difficult = Column(Integer, server_default="0", nullable=False)
    task = Column(Text)



