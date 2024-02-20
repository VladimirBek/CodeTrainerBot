from arq import cron
from arq.connections import RedisSettings

from app.config import settings
from app.logs import logger
from app.rq.parser import parse_tasks
from app.src import exercise_parser


async def after_job_end(ctx):
    logger.info(f'Job End with {ctx}')
    return ctx


class WorkerSettings:
    cron_jobs = [cron(parse_tasks, minute=1, run_at_startup=True)]
    queue_name = "parse_tasks"
    after_job_end = after_job_end
    job_timeout = 60 * 60 * 3

    ctx = {"parser": exercise_parser}
    redis_settings = RedisSettings(host=settings.REDIS_HOST, port=settings.REDIS_PORT, conn_retry_delay=5,
                                   conn_retries=20)
