import logging
import sys

from fastapi import FastAPI
from starlette.responses import RedirectResponse

import routes



app = FastAPI(
    title='Mvideo Monitoring Service',
    version='1.0.0',
    description='Тестовое задание для Центра Кибербезопасности',
)

app.include_router(routes.product_info)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
stream_handler = logging.StreamHandler(sys.stdout)
log_formatter = logging.Formatter('%(asctime)s [%(processName)s: %(process)d] [%(threadName)s: %(thread)d] [%(levelname)s] %(name)s: %(message)s')
stream_handler.setFormatter(log_formatter)
logger.addHandler(stream_handler)
logger.info('Monitoriong is starting...')


@app.get('/')
async def index():
    return RedirectResponse('/docs')


if __name__ == '__main__':
    app = app
