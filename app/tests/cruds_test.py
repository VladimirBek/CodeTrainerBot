import asyncio
import unittest
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.cruds.crud_category import CRUDCategory
from app.cruds.crud_excercise import CRUDExercise
from app.cruds.crud_level import CRUDLevel
from app.models import Category, Exercise, Level
from app.schemas import CategorySchemaCreate, ExerciseSchemaCreate, LevelSchemaCreate

engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=True, future=True)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


class TestCRUDCategory(unittest.TestCase):

    async def create_test_data(self, session):
        category1 = CategorySchemaCreate(name="Category 1")
        category2 = CategorySchemaCreate(name="Category 2")
        session.add(category1)
        session.add(category2)
        await session.commit()

    async def test_get_by_name(self):
        async with async_session() as session:
            await self.create_test_data(session)
            crud = CRUDCategory(Category)
            category = await crud.get_by_name(session, name="Category 1")
            self.assertEqual(category.name, "Category 1")

    async def test_get_by_name_not_found(self):
        async with async_session() as session:
            await self.create_test_data(session)
            crud = CRUDCategory(Category)
            category = await crud.get_by_name(session, name="Non-existent Category")
            self.assertIsNone(category)

class TestCRUDExercise(unittest.TestCase):

    async def create_test_data(self, session):
        exercise1 = ExerciseSchemaCreate(cf_id="1", topic_id=1, difficult=1)
        exercise2 = ExerciseSchemaCreate(cf_id="2", topic_id=1, difficult=2)
        exercise3 = ExerciseSchemaCreate(cf_id="3", topic_id=2, difficult=1)
        session.add(exercise1)
        session.add(exercise2)
        session.add(exercise3)
        await session.commit()

    async def test_get_by_cf_id(self):
        async with async_session() as session:
            await self.create_test_data(session)
            crud = CRUDExercise(Exercise)
            exercise = await crud.get_by_cf_id(session, cf_id="1")
            self.assertEqual(exercise.cf_id, "1")

    async def test_get_by_category_id(self):
        async with async_session() as session:
            await self.create_test_data(session)
            crud = CRUDExercise(Exercise)
            exercises = await crud.get_by_category_id(session, topic_id=1)
            self.assertEqual(len(exercises), 2)

    async def test_get_by_difficulty(self):
        async with async_session() as session:
            await self.create_test_data(session)
            crud = CRUDExercise(Exercise)
            exercises = await crud.get_by_difficulty(session, difficult=1)
            self.assertEqual(len(exercises), 2)

    async def test_get_by_difficulty_and_topic(self):
        async with async_session() as session:
            await self.create_test_data(session)
            crud = CRUDExercise(Exercise)
            exercises = await crud.get_by_difficulty_and_topic(session, difficulty=1, topic_id=1)
            self.assertEqual(len(exercises), 1)
            self.assertEqual(exercises[0].cf_id, "1")


class TestCRUDLevel(unittest.TestCase):

    async def create_test_data(self, session):
        level1 = LevelSchemaCreate(difficult=1)
        level2 = LevelSchemaCreate(difficult=2)
        session.add(level1)
        session.add(level2)
        await session.commit()

    async def test_get_by_level(self):
        async with async_session() as session:
            await self.create_test_data(session)
            crud = CRUDLevel(Level)
            level = await crud.get_by_level(session, difficult=1)
            self.assertEqual(level.difficult, 1)

    async def test_get_by_level_not_found(self):
        async with async_session() as session:
            await self.create_test_data(session)
            crud = CRUDLevel(Level)
            level = await crud.get_by_level(session, difficult=3)
            self.assertIsNone(level)

if __name__ == "__main__":
    unittest.main()
