import datetime

from aiogram import Router, F, html
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from .keyboard import get_products_keyboard, get_product_details_keyboard
from .service import ApiService
from .utils import breakup_message


router = Router()

@router.message(Command('help'))
async def cmd_help(message: Message) -> None:
    msg = ('Use /products to view tracked products or enter a url to add a new product. '
           'The url should contain the \'www.mvideo.ru\' domain')
    await message.answer(msg)


@router.message(F.text.contains('www.mvideo.ru'))
async def cmd_add_product(message: Message, api_service: ApiService) -> None:
    product = await api_service.add_product(message.text)
    if product:
        await message.answer('Product will be added')
    else:
        await message.answer('Invalid url', show_alert=True)


@router.message(Command('products'))
async def cmd_products(message: Message, api_service: ApiService) -> None:
    products = await api_service.get_products()
    if products:
        keyboard = get_products_keyboard(products)
        msg = html.bold('Tracked Products:')
        for index, product in enumerate(products, start=1):
            msg += f"\n<b>{index}.</b> {product['title']}"
        await message.answer(msg, reply_markup=keyboard)
    else:
        await message.answer('No products at the moment')


@router.callback_query(F.data.startswith('detail:'))
async def cb_product_detail(callback: CallbackQuery, api_service: ApiService) -> None:
    product_id = int(callback.data.split(':')[1])
    details = await api_service.get_details(product_id)
    product = sorted(details, key=lambda x: x['date'], reverse=True)[0]

    title = product['product']['title']
    price = str(product['value']) + ' ₽'
    description = breakup_message(product['product']['description'])
    rating = str(product['product']['rating']) if product['product']['rating'] is not None else 'n/a'
    link = product['product']['link']

    if product:
        await callback.message.answer(f'{html.bold("Product:")}\n{title}\n{html.bold("Price:")} {price}\n{html.bold("Rating:")} {rating}')
        await callback.message.answer(f'{html.bold("Link:")} {link}')
        while len(description) > 1:
            await callback.message.answer(description.pop(0))
        await callback.message.answer(description.pop(0), reply_markup=get_product_details_keyboard(product))
    else:
        await callback.message.answer('Product not found', show_alert=True)

@router.callback_query(F.data.startswith('delete:'))
async def cb_product_delete(callback: CallbackQuery, api_service: ApiService) -> None:
    product_id = int(callback.data.split(':')[1])
    await api_service.delete_product(product_id)
    await callback.message.answer('Product deleted')


@router.callback_query(F.data.startswith('price:'))
async def cb_product_prices(callback: CallbackQuery, api_service: ApiService) -> None:
    product_id = int(callback.data.split(':')[1])
    details = await api_service.get_details(product_id)
    data = sorted(details, key=lambda x: x['date'], reverse=True)
    prices = '\n'.join([
        f'<b>{index}. Price:</b> {item["value"]} ₽ '
        f'<b>Added at:</b> {datetime.datetime.fromisoformat(item["date"]).strftime("%Y-%m-%d %H:%M:%S")}'
        for index, item in enumerate(data, start=1)
    ])
    await callback.message.answer(f'{html.bold("Price History:")}\n{prices}')
