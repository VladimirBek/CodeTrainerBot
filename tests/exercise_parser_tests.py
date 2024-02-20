import unittest

from app.src.exercise_parser import ExerciseParser

events = []


class TestSParserMethods(unittest.IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        self._async_connection = ExerciseParser()
        events.append(self._async_connection)

    async def test_get_exercises(self):
        result = await self._async_connection.get_urls()
        self.assertIsInstance(result, list[str])
