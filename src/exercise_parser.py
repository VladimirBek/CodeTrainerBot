import asyncio

from config import settings
from requests_html import AsyncHTMLSession, HTMLResponse
from fake_useragent import UserAgent

from logs import logger


class ExerciseParser:
    __slots__ = 'base_url', "user_agent", "session"

    def __init__(self):
        self.base_url = settings.CODEFORCE_API_URL
        self.user_agent = UserAgent().random
        self.session = AsyncHTMLSession()

    async def get_urls(self):
        resp = await self.session.get(self.base_url + 'problemset', params={'order': "BY_SOLVED_DESC"},
                                      headers={'User-Agent': self.user_agent})
        if resp.status_code != 200:
            logger.error(f'Problem with getting urls of pages: {resp.status_code}')
            return []
        max_page = resp.html.find('span.page-index')[-1].text
        urls = [self.base_url + 'problemset/page/' + str(i) for i in range(1, int(max_page) + 1)]
        return urls

    async def parse_exercises(self, urls):
        exercises = []
        for url in urls:
            resp = await self.session.get(url, headers={'User-Agent': self.user_agent})
            if resp.status_code != 200:
                logger.error(f'Problem with getting urls of page: {url}, status code: {resp.status_code}')
                continue
            await self.parse_exercise(resp)
            await asyncio.sleep(1)
        #
        #     exercises.extend(resp.html.find('div.problem-statement'))
        #     print(exercises)
        # return exercises

    async def parse_exercise(self, response: HTMLResponse):
        table_with_problems = response.html.find("table.problems")
        rows = table_with_problems[0].find('tr')
        for row in rows:
            pass

async def main():
    ex_parser = ExerciseParser()
    urls = await ex_parser.get_urls()
    await ex_parser.parse_exercises(urls)





if __name__ == '__main__':
    asyncio.run(main())
