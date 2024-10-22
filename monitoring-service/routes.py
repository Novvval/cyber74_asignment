from fastapi import APIRouter
from starlette.responses import JSONResponse
from worker import find_product_info

product_info = APIRouter(prefix='/product_info')


@product_info.post('/')
async def add_product(link: str, scheme: str = 'create'):
    if not link.startswith('https://'):
        link = 'https://' + link
    task = find_product_info.delay(link, scheme)
    return JSONResponse({'task': task.id})


@product_info.get('/{task_id}')
async def get_task_status(task_id: str):
    task = find_product_info.AsyncResult(task_id)
    if task.state == 'SUCCESS':
        return JSONResponse({'status': task.state, 'result': task.result})
    else:
        return JSONResponse({'status': task.state})
