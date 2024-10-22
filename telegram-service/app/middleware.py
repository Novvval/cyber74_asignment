from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from typing import Any, Awaitable, Callable, Dict

from .service import ApiService

class ApiServiceMiddleware(BaseMiddleware):
    def __init__(self, api_service: ApiService):
        self.api_service = api_service

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        data['api_service'] = self.api_service
        return await handler(event, data)
