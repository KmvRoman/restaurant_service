from typing import Optional, Any

from aiogram import Bot
from aiogram.filters import Filter
from aiogram.types import ChatMemberUpdated, User
from aiogram.enums.chat_member_status import ChatMemberStatus


class RestrictAdmin(Filter):
    def __init__(self, name: Optional[str] = None) -> None:
        self.name = name

    async def __call__(
        self,
        message: ChatMemberUpdated,
        event_from_user: User,
        bot: Bot,
    ) -> bool | dict[str, Any]:
        if message.new_chat_member.status in [
            ChatMemberStatus.MEMBER, ChatMemberStatus.KICKED,
            ChatMemberStatus.RESTRICTED, ChatMemberStatus.LEFT,
        ] and message.from_user.is_bot is not True:
            return True
