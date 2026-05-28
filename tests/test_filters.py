import asyncio
from types import SimpleNamespace

from rctl_bot.filters import AdminFilter, PrivateChatFilter


def run(coro):
    return asyncio.run(coro)


def message(user_id: int | None, chat_type: str):
    user = None if user_id is None else SimpleNamespace(id=user_id)
    chat = SimpleNamespace(type=chat_type)
    return SimpleNamespace(from_user=user, chat=chat)


def test_admin_filter_accepts_only_configured_admins() -> None:
    filter_ = AdminFilter(frozenset({1001, 1002}))

    assert run(filter_(message(1001, "private"))) is True
    assert run(filter_(message(9000, "private"))) is False
    assert run(filter_(message(None, "private"))) is False


def test_private_chat_filter_accepts_only_private_chats() -> None:
    filter_ = PrivateChatFilter()

    assert run(filter_(message(1001, "private"))) is True
    assert run(filter_(message(1001, "group"))) is False
    assert run(filter_(message(1001, "supergroup"))) is False
