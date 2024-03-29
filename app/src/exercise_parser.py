import asyncio
import random

from fake_useragent import UserAgent
from requests_html import HTMLSession

from app.config import settings
from app.cruds.crud_category import crud_category
from app.cruds.crud_excercise import crud_exercise
from app.cruds.crud_level import crud_level
from app.logs import logger
from app.schemas import ExerciseSchemaCreate, LevelSchemaCreate
from app.schemas.category_schema import CategorySchemaCreate


class ExerciseParser:
    __slots__ = 'base_url', "user_agent", "session"

    def __init__(self):
        self.base_url = settings.CODEFORCE_API_URL
        self.user_agent = UserAgent().random
        self.session = HTMLSession()

    async def get_urls(self):
        resp = self.session.get(self.base_url + 'problemset', params={'order': "BY_SOLVED_DESC", "locale": "ru"},
                                headers={'User-Agent': self.user_agent})
        if resp.status_code != 200:
            logger.error(f'Problem with getting urls of pages: status code {resp.status_code}')
            return []
        max_page = resp.html.find('span.page-index')[-1].text
        urls = [self.base_url + 'problemset/page/' + str(i) for i in range(1, int(max_page) + 1)]
        return urls

    async def parse_pages(self, db, urls):
        for url in urls:
            logger.info(f'Parsing page: {url}')
            resp = self.session.get(url, headers={'User-Agent': self.user_agent},
                                    params={'order': "BY_SOLVED_DESC", "locale": "ru"})
            if resp.status_code != 200:
                logger.error(f'Problem with getting urls of page: {url}, status code: {resp.status_code}')
                continue
            await self.get_rows(resp, db)
            logger.info(f'Page {url} parsed')

    async def get_rows(self, response, db):
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

                topic_name = random.choice(topic)
                topic_name = topic_name.split(',')[0].strip()
                topic_in_db = await crud_category.get_by_name(db, name=topic_name)
                if topic_in_db:
                    topic_id = topic_in_db.id
                else:
                    new_topic = await crud_category.create(db, obj_in=CategorySchemaCreate(name=topic_name))
                    topic_id = new_topic.id
                task_text = await self.get_task(url)
                count_solved = int(td[4].text[1:])
                difficult = td[3].text
                if difficult.isdigit():
                    int_difficult = int(difficult)
                    level_indb = await crud_level.get_by_level(db, difficult=int_difficult)
                    if level_indb:
                        level_id = level_indb.id
                    else:
                        level = await crud_level.create(db, obj_in=LevelSchemaCreate(difficult=difficult))
                        level_id = level.id
                else:
                    level_id = 1

                obj_in = ExerciseSchemaCreate(
                    cf_id=cf_id,
                    url=url,
                    name=name,
                    count_solved=count_solved,
                    difficult=level_id,
                    topic_id=topic_id,
                    task=task_text
                )
                await crud_exercise.create(db, obj_in=obj_in)
                logger.info(f'Exercise {name} with id {cf_id} created')
            except Exception as e:
                logger.error(e)
            await asyncio.sleep(0.5)

    async def get_task(self, url):
        task = self.session.get(url, headers={'User-Agent': self.user_agent})
        task_statement = task.html.find("div.problem-statement")
        text = task_statement[0].find('p')
        text = [p.text for p in text]
        return '\n'.join(text)


exercise_parser = ExerciseParser()
