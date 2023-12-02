from contextlib import suppress

from aiogram.enums.chat_member_status import ChatMemberStatus
from aiogram.exceptions import TelegramBadRequest
from aiogram import types, Bot, Router, F

from src.application.promote_user.dto import PromoteUserDtoInput
from src.application.read_detached_branches.dto import ReadDetachedBranchesDtoInput
from src.domain.restaurant.entities.restaurant_view import RestaurantId
from src.domain.user.constants.user import Member
from src.infrastructure.database.repositories.user_repository import UserRepository
from src.infrastructure.ioc.interfaces import InteractorFactory
from src.presentation.bot.content.fasade.interfaces import IContent
from src.presentation.bot.filters.admin.add_group import MatchGroupToBranch
from src.presentation.bot.filters.admin.promote import PromoteAdmin
from src.presentation.bot.filters.admin.remind_promote_bot_to_admin import RemindPromoteBotToAdmin
from src.presentation.bot.filters.admin.remove_from_group import UnmatchGroupFromBranch
from src.presentation.bot.filters.admin.restrict import RestrictAdmin

promote = Router()


@promote.chat_member(PromoteAdmin())
async def administrator_arrived(
        message: types.ChatMemberUpdated, bot: Bot, content: IContent,
        ioc: InteractorFactory, user_repo: UserRepository,
):
    user = await user_repo.get_user_by_telegram_id(telegram_id=message.new_chat_member.user.id)
    if user is None:
        return
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
    if user is None:
        return
    promote_user = await ioc.promote_user()
    await promote_user(data=PromoteUserDtoInput(user_id=user.id, member=Member.user))
    await bot.send_message(
        chat_id=message.chat.id,
        text=content.text.admin_restricted_to_user(mention=message.new_chat_member.user.mention_html()),
    )


@promote.message(F.text == "update_admins")
async def update_admins_manually(
        message: types.Message, bot: Bot, content: IContent,
        ioc: InteractorFactory, user_repo: UserRepository,
):
    administrators = await bot.get_chat_administrators(chat_id=message.chat.id)
    promote_user = await ioc.promote_user()
    for admin in administrators:
        user = await user_repo.get_user_by_telegram_id(telegram_id=admin.user.id)
        if user is None:
            continue
        if admin.status in [ChatMemberStatus.CREATOR, ChatMemberStatus.ADMINISTRATOR]:
            await promote_user(data=PromoteUserDtoInput(user_id=user.id, member=Member.administrator))
        else:
            await promote_user(data=PromoteUserDtoInput(user_id=user.id, member=Member.user))
    await bot.send_message(chat_id=message.chat.id, text=content.text.administrators_updated())


@promote.my_chat_member(RemindPromoteBotToAdmin())
async def update_group_by_branch(message: types.ChatMemberUpdated, bot: Bot, content: IContent):
    await bot.send_message(chat_id=message.chat.id, text=content.text.remind_promote_bot_to_admin())


@promote.my_chat_member(MatchGroupToBranch())
async def update_group_by_branch(
        message: types.ChatMemberUpdated, bot: Bot, content: IContent,
        ioc: InteractorFactory, restaurant: RestaurantId,
):
    read_branches = await ioc.read_detached_branches()
    branches = await read_branches(data=ReadDetachedBranchesDtoInput(restaurant_id=restaurant))
    await bot.send_message(
        chat_id=message.chat.id, text=content.text.select_branches_attach_group(),
        reply_markup=content.inline.groups_match_with_branches(buttons=branches)
    )


@promote.callback_query(F.data.startswith("match_"))
async def match_group(
        call: types.CallbackQuery, bot: Bot, content: IContent,
        user_repo: UserRepository,
):
    restaurant_location_id = int(call.data.split("_")[1])
    await user_repo.attach_group_to_branch(
        restaurant_location_id=restaurant_location_id, group_id=call.message.chat.id)
    with suppress(TelegramBadRequest):
        await bot.edit_message_reply_markup(
            chat_id=call.message.chat.id, message_id=call.message.message_id,
            reply_markup=content.inline.groups_match_with_branches(buttons=[]),
        )
    await bot.send_message(chat_id=call.message.chat.id, text=content.text.attached_group())
    await call.answer()


@promote.my_chat_member(UnmatchGroupFromBranch())
async def detach_group(message: types.ChatMemberUpdated, user_repo: UserRepository):
    await user_repo.detach_group(group_id=message.chat.id)
