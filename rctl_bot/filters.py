from aiogram.enums import ChatType
from aiogram.filters import Filter
from aiogram.types import Message


class AdminFilter(Filter):
    def __init__(self, admin_telegram_ids: frozenset[int]) -> None:
        self.admin_telegram_ids = admin_telegram_ids

    async def __call__(self, message: Message) -> bool:
        return message.from_user is not None and message.from_user.id in self.admin_telegram_ids


class PrivateChatFilter(Filter):
    async def __call__(self, message: Message) -> bool:
        return message.chat.type == ChatType.PRIVATE or message.chat.type == "private"
