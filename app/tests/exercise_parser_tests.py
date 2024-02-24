from unittest.mock import MagicMock

import pytest

from app.src.exercise_parser import ExerciseParser


@pytest.mark.asyncio
async def test_get_urls():
    exercise_parser = ExerciseParser()
    exercise_parser.session.get = MagicMock(return_value=MagicMock(status_code=200, html=MagicMock(find=lambda x: [MagicMock(text='10')])))

    urls = await exercise_parser.get_urls()
    assert len(urls) == 10


@pytest.mark.asyncio
async def test_get_rows():
    exercise_parser = ExerciseParser()
    exercise_parser.get_task = MagicMock(return_value='Test task text')

    mock_db = MagicMock()
    mock_db.execute = MagicMock()

    exercise_parser.session.get = MagicMock(return_value=MagicMock(status_code=200, html=MagicMock(find=lambda x: [MagicMock(find=lambda x: ['Test statement'])])))

    await exercise_parser.get_rows(MagicMock(), ['mock_url'])

    assert exercise_parser.get_task.call_count == 1
    assert mock_db.execute.call_count == 1
