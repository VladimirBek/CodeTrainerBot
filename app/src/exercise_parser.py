import asyncio
import random

from fake_useragent import UserAgent
from requests_html import AsyncHTMLSession, HTMLResponse
from sqlalchemy import AsyncSession

from app.config import settings
from app.cruds.crud_category import crud_category
from app.cruds.crud_excercise import crud_exercise
from app.logs import logger
from app.schemas import ExerciseSchemaCreate
from app.schemas.category_schema import CategorySchemaCreate


class ExerciseParser:
    __slots__ = 'base_url', "user_agent", "session"

    def __init__(self):
        self.base_url = settings.CODEFORCE_API_URL
        self.user_agent = UserAgent().random
        self.session = AsyncHTMLSession()

    async def get_urls(self):
        resp = await self.session.get(self.base_url + 'problemset', params={'order': "BY_SOLVED_DESC", "locale": "ru"},
                                      headers={'User-Agent': self.user_agent})
        if resp.status_code != 200:
            logger.error(f'Problem with getting urls of pages: status code {resp.status_code}')
            return []
        max_page = resp.html.find('span.page-index')[-1].text
        urls = [self.base_url + 'problemset/page/' + str(i) for i in range(1, int(max_page) + 1)]
        return urls

    async def parse_pages(self, db, urls):
        for url in urls:
            resp = await self.session.get(url, headers={'User-Agent': self.user_agent},
                                          params={'order': "BY_SOLVED_DESC", "locale": "ru"})
            if resp.status_code != 200:
                logger.error(f'Problem with getting urls of page: {url}, status code: {resp.status_code}')
                continue
            await self.get_rows(resp, db)

    async def get_rows(self, response: HTMLResponse, db: AsyncSession):
        table_with_problems = response.html.find("table.problems")
        rows = table_with_problems[0].find('tr')
        for row in rows:
            try:
                td = row.find('td')
                if len(td) == 0:
                    continue
                url = self.base_url + td[0].find('a', first=True).attrs.get('href')
                cf_id = td[0].find('a', first=True).text
                excercise_indb = await crud_exercise.get_by_cf_id(db, cf_id=cf_id)
                if excercise_indb:
                    continue
                name, *topic = td[1].text.split("\n")
                topic = random.choice(topic)
                topic_in_db = await crud_category.get_by_name(db, name=topic)
                if topic_in_db:
                    topic_id = topic_in_db.id
                else:
                    new_topic = await crud_category.create(db, obj_in=CategorySchemaCreate(name=topic))
                    topic_id = new_topic.id
                name = td[0].find('a', first=True).text
                task_text = await self.get_task(url)
                count_solved = int(td[4].text[1:])
                difficult = td[3].text
                obj_in = ExerciseSchemaCreate(
                    cf_id=cf_id,
                    url=url,
                    name=name,
                    count_solved=count_solved,
                    difficult=difficult,
                    topic_id=topic_id,
                    task=task_text
                )
                await crud_exercise.create(db, obj_in=obj_in)
            except Exception as e:
                logger.error(e)
            await asyncio.sleep(0.5)

    async def get_task(self, url):
        task = await self.session.get(url, headers={'User-Agent': self.user_agent})
        task_statement = task.html.find("div.problem-statement")
        text = task_statement[0].find('p')
        text = [p.text for p in text]
        return '\n'.join(text)


exercise_parser = ExerciseParser()
