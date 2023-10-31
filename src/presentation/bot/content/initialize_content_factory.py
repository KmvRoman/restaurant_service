from src.domain.user.constants.user import Language
from src.infrastructure.database.repositories.user_repository import UserRepository
from src.presentation.bot.content.fasade.ru import ContentRu
from src.presentation.bot.content.fasade.uz import ContentUz
from src.presentation.bot.content.format.amount_format import FormatAmount
from src.presentation.bot.content.format.format_manager import FormatManager
from src.presentation.bot.content.format.name_format import TextFormat
from src.presentation.bot.content.get_implement import LanguageManager
from src.presentation.bot.content.text_content.keyboard_content.inline.ru import RussianInlineKeyboardText
from src.presentation.bot.content.text_content.keyboard_content.inline.uz import UzbekInlineKeyboardText
from src.presentation.bot.content.text_content.keyboard_content.reply.ru import RussianReplyKeyboardText
from src.presentation.bot.content.text_content.keyboard_content.reply.uz import UzbekReplyKeyboardText
from src.presentation.bot.content.text_content.ru import RussianText
from src.presentation.bot.content.text_content.uz import UzbekText
from src.presentation.bot.keyboards.inline_keyboard import InlineKeyboard
from src.presentation.bot.keyboards.reply_keyboard import ReplyKeyboard


def initialize_content(user_repo: UserRepository) -> LanguageManager:
    formats = [
        FormatAmount(),
        TextFormat(),
    ]
    format_manager = FormatManager(formatters=formats)
    content = [
        ContentRu(
            language=Language.ru,
            text=RussianText(format=format_manager),
            inline=RussianInlineKeyboardText(user_repo=user_repo, inline_keyboard=InlineKeyboard()),
            reply=RussianReplyKeyboardText(reply_keyboard=ReplyKeyboard()),
        ),
        ContentUz(
            language=Language.uz,
            text=UzbekText(format=format_manager),
            inline=UzbekInlineKeyboardText(user_repo=user_repo, inline_keyboard=InlineKeyboard()),
            reply=UzbekReplyKeyboardText(reply_keyboard=ReplyKeyboard()),
        )
    ]
    language_manager = LanguageManager(implements=content)
    return language_manager
