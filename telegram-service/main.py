import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message

from app.handlers import router
from app.middleware import ApiServiceMiddleware
from app.service import ApiService
from app.utils import set_commands
from config import Config


dp = Dispatcher()


@dp.message(CommandStart())
async def cmd_start(message: Message) -> None:
    await message.answer(f'Hello! I am a bot that tracks products from mvideo.ru. Type /help to see my commands')


async def main() -> None:
    bot = Bot(token=Config.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await set_commands(bot)

    api_service = ApiService()

    dp.message.middleware(ApiServiceMiddleware(api_service))
    dp.callback_query.middleware(ApiServiceMiddleware(api_service))

    dp.include_router(router)

    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
