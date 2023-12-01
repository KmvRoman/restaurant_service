from aiogram import types, Bot, Router, F
from aiogram.enums.chat_member_status import ChatMemberStatus

from src.application.promote_user.dto import PromoteUserDtoInput
from src.domain.user.constants.user import Member
from src.domain.user.entities.user import User
from src.infrastructure.database.repositories.user_repository import UserRepository
from src.infrastructure.ioc.interfaces import InteractorFactory
from src.presentation.bot.content.fasade.interfaces import IContent
from src.presentation.bot.filters.admin.promote import PromoteAdmin
from src.presentation.bot.filters.admin.restrict import RestrictAdmin

promote = Router()


@promote.chat_member(PromoteAdmin())
async def administrator_arrived(
        message: types.ChatMemberUpdated, bot: Bot, content: IContent,
        ioc: InteractorFactory, user_repo: UserRepository,
):
    user = await user_repo.get_user_by_telegram_id(telegram_id=message.new_chat_member.user.id)
    promote_user = await ioc.promote_user()
    await promote_user(data=PromoteUserDtoInput(user_id=user.id, member=Member.administrator))
    await bot.send_message(
        chat_id=message.chat.id,
        text=content.text.user_promoted_to_admin(mention=message.new_chat_member.user.mention_html()),
    )


@promote.chat_member(RestrictAdmin())
async def administrator_restricted(
        message: types.ChatMemberUpdated, bot: Bot, content: IContent,
        ioc: InteractorFactory, user_repo: UserRepository,
):
    user = await user_repo.get_user_by_telegram_id(telegram_id=message.new_chat_member.user.id)
    promote_user = await ioc.promote_user()
    await promote_user(data=PromoteUserDtoInput(user_id=user.id, member=Member.user))
    await bot.send_message(
        chat_id=message.chat.id,
        text=content.text.admin_restricted_to_user(mention=message.new_chat_member.user.mention_html()),
    )


@promote.message()
async def update_admins_manually(message: types.Message, bot: Bot, content: IContent, ioc: InteractorFactory):
    print(message)


@promote.my_chat_member()
async def update_group_by_branch(message: types.ChatMemberUpdated, bot: Bot, content: IContent, ioc: InteractorFactory):
    pass
