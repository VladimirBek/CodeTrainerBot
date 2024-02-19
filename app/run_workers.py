import asyncio

from arq.worker import create_worker

from app.rq.workers.parser_worker import WorkerSettings


async def main():
    worker_parser = create_worker(WorkerSettings)
    await worker_parser.async_run()

if __name__ == '__main__':
    asyncio.run(main())