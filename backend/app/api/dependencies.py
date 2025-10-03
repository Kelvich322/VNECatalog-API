from app.database import async_session

async def get_db():
    """
    Генератор ассинхронных сессий БД.
    """
    async with async_session() as session:
        yield session