from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_products_keyboard(products) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for index, product in enumerate(products, start=1):
        builder.add(InlineKeyboardButton(
            text=f'View product {index}',
            callback_data=f'detail:{product["id"]}'
        ))
    builder.adjust(2)
    return builder.as_markup()

def get_product_details_keyboard(product) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(
        text='Price History',
        callback_data=f'price:{product["product"]["id"]}'
    ))
    builder.add(InlineKeyboardButton(
        text='Delete',
        callback_data=f'delete:{product["product"]["id"]}'
    ))
    builder.adjust(2)
    return builder.as_markup()
