from celery import Celery
from celery.schedules import crontab

import httpx

from config import Config
from depends import get_service


celery = Celery(__name__)
celery.conf.broker_url = Config.BROKER_URL
celery.conf.result_backend = Config.CELERY_RESULT_BACKEND
celery.conf.timezone = 'UTC'

api_url = Config.API_URL


@celery.on_after_configure.connect
def setup_scheduled_task(sender, **kwargs) -> None:
    sender.add_periodic_task(crontab(minute=0, hour='*'), scheduled_scraping)


@celery.task(name="find product info")
def find_product_info(link: str, scheme: str = 'create') -> dict:
    service = get_service()
    with service.driver_context():
        result = service.find_product(link)

    if scheme == 'create':
        httpx.post(f'{api_url}/product/?link={result["link"]}', json=result)
    elif scheme == 'update':
        httpx.put(f'{api_url}/product/?link={result["link"]}', json=result)

    return result


@celery.task(name='update prices')
def update_prices(links: list) -> None:
    service = get_service()
    with service.driver_context():
        for link in links:
            result = service.find_product(link)
            httpx.put(f'{api_url}/product/?link={result["link"]}', json=result)


@celery.task(name='check prices')
def scheduled_scraping() -> None:
    url = Config.API_URL
    response = httpx.get(f'{url}/product/list')
    if response.status_code == 200:
        links = list(map(lambda x: 'https://' + x['link'], response.json()))
        update_prices.delay(links)
