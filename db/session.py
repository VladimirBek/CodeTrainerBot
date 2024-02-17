from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from config import settings

engine = create_async_engine(str(settings.SQLALCHEMY_DATABASE_URI), pool_pre_ping=True, pool_size=60, max_overflow=100)
LocalSession = async_sessionmaker(engine, expire_on_commit=False)
