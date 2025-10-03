from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import engine, init_db
from app.api.routers.product import product_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Асинхронный контекстный менеджер жизненного цикла приложения FastAPI.
    Выполняет инициализацию при запуске приложения и очистку при завершении.
    """
    import app.models # type: ignore # noqa

    await init_db()
    yield
    await engine.dispose()


app = FastAPI(lifespan=lifespan)
app.include_router(product_router)