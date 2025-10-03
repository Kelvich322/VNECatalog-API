from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base


DATABASE_URL = "postgresql+asyncpg://user:password@db:5432/vnecatalog"

engine = create_async_engine(DATABASE_URL)
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()


async def init_db():
    """
    Функция инициализации базы данных.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)