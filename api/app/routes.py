from urllib.parse import urlparse

import httpx
from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from pydantic import json
from starlette.responses import JSONResponse
from starlette.status import HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST

from .models import Product, Price, ProductInfoSchema
from .repository import Repository
from depends import get_repository
from config import Config


RESPONSES = {
    200: {'detail': 'Deleted'},
    400: {'detail': 'Bad Request'},
    404: {'detail': 'Not Found'}
}

monitoring_url = Config.MONITORING_URL

product = APIRouter(prefix="/product")
price = APIRouter(prefix="/price")


@product.get('/list', response_model=list[Product], responses=RESPONSES)
async def get_list(
        limit=None,
        offset=None,
        repository: Repository = Depends(get_repository)
):
    async with repository.session_context():
        return await repository.get_many(Product, limit=limit, offset=offset)


@product.get('/', response_model=Product, responses=RESPONSES)
async def get_product_by_link(link: str, repository: Repository = Depends(get_repository)):
    link = urlparse(link)
    async with repository.session_context():
        result = await repository.get_one(Product, Product.link == link.path)
        if result is not None:
            return result
        else:
            raise HTTPException(status_code=HTTP_404_NOT_FOUND)

@product.get('/{product_id}', response_model=Product, responses=RESPONSES)
async def get_product_by_link(product_id: int, repository: Repository = Depends(get_repository)):
    async with repository.session_context():
        result = await repository.get_one(Product, Product.id == product_id)
        if result is not None:
            return result
        else:
            raise HTTPException(status_code=HTTP_404_NOT_FOUND)


@product.post('/', response_model=Price, responses=RESPONSES)
async def add_product(link: str, product_info: ProductInfoSchema = None, repository: Repository = Depends(get_repository)):
    """
    **Usage**:
    - with body: Add new product and price
    - without body: Triggers the monitoring service to search for product info using the provided link

    *Only links with domain www.mvideo.ru are supported*
    """
    link = 'https://' + link if not link.startswith('https://') else link
    if link.find('www.mvideo.ru') < 0:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail='Invalid link. Only links starting with www.mvideo.ru are supported'
        )

    async with repository.session_context():
        if await repository.get_one(Product, Product.link == link.split('https://')[-1]) is not None:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail='Product already exists')
        if product_info is None:
            async with httpx.AsyncClient() as client:
                await client.post(f'{monitoring_url}/product_info/?link={link}')
            return JSONResponse({'detail': f'Product will be added soon. Check at GET /product/?link={link}'})

        product = Product(
            link=product_info.link,
            title=product_info.title,
            description=product_info.description,
            rating=product_info.rating
        )
        price = Price(value=product_info.value, product=product)
        result = await repository.add([product, price])
        return result[1]

    raise HTTPException(status_code=HTTP_404_NOT_FOUND)

@product.put('/', response_model=Price, responses=RESPONSES)
async def update_product(link: str, product_info: ProductInfoSchema = None, repository: Repository = Depends(get_repository)):
    async with repository.session_context():
        link = link.split('//')[-1]
        product = await repository.get_one(Product, Product.link == link)
        if product is not None:
            product.title = product_info.title
            product.description = product_info.description
            product.rating = product_info.rating
            price = Price(value=product_info.value, product=product)
            result = await repository.add([product, price])
        return result[1]


@product.delete('/{product_id}', responses=RESPONSES)
async def delete_product(product_id: int, repository: Repository = Depends(get_repository)):
    async with repository.session_context():
        product = await repository.get_one(Product, Product.id == product_id)
        if product is not None:
            await repository.delete(product)
            return JSONResponse({"message": "Deleted"})
        else:
            raise HTTPException(status_code=HTTP_404_NOT_FOUND)


@price.get('/', response_model=list[Price], responses=RESPONSES)
async def get_prices_by_link(link: str, repository: Repository = Depends(get_repository)):
    link = link.split('//')[-1]
    async with repository.session_context():
        prices = await repository.get_prices(Product.link == link)

        if prices is not None:
            return prices
        else:
            raise HTTPException(status_code=HTTP_404_NOT_FOUND)


@price.get('/{product_id}', response_model=list[Price], responses=RESPONSES)
async def get_prices_by_product_id(product_id: int, repository: Repository = Depends(get_repository)):
    async with repository.session_context():
        prices = await repository.get_prices(Product.id == product_id)

        if prices is not None:
            return prices
        else:
            raise HTTPException(status_code=HTTP_404_NOT_FOUND)

@price.post('/', response_model=list[Price], responses=RESPONSES)
async def add_prices(prices: str, repository: Repository = Depends(get_repository)):
    async with repository.session_context():
        prices = json.loads(prices)
        links = set(map(lambda x: x['link'], prices))
        existing_products = await repository.get_many(Product, Product.link.in_(links))
        result = []
        for product in existing_products:
            price = next(filter(lambda x: x['link'] == product.link, prices))
            result.append(Price(value=price['price'], product=product))

        await repository.add(result)

        if prices is not None:
            return prices
        else:
            raise HTTPException(status_code=HTTP_404_NOT_FOUND)