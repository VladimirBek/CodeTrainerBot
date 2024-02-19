from app.db import LocalSession


async def parse_tasks(ctx):
    async with LocalSession() as db:
        parser = ctx["parser"]
        urls = await parser.get_urls()
        await parser.parse_pages(db, urls)
