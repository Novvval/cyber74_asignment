import logging
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

from contextlib import asynccontextmanager

from fastapi import FastAPI
from starlette.responses import RedirectResponse

from depends import engine
from app import orm, routes


@asynccontextmanager
async def lifespan(app: FastAPI):
    orm.init_mappers()
    await orm.create_tables(engine)
    yield


app = FastAPI(
    lifespan=lifespan,
    title='Mvideo monitoring API',
    version='1.0.0',
    description='Тестовое задание для Центра Кибербезопасности',
)

app.include_router(routes.product)
app.include_router(routes.price)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
stream_handler = logging.StreamHandler(sys.stdout)
log_formatter = logging.Formatter('%(asctime)s [%(processName)s: %(process)d] [%(threadName)s: %(thread)d] [%(levelname)s] %(name)s: %(message)s')
stream_handler.setFormatter(log_formatter)
logger.addHandler(stream_handler)
logger.info('API is starting...')


@app.get('/')
async def index():
    return RedirectResponse('/docs')


if __name__ == '__main__':
    app = app
