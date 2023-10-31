from dataclasses import dataclass

from src.domain.user.constants.user import Language
from src.presentation.bot.content.text_content.interfaces import IText
from src.presentation.bot.content.text_content.keyboard_content.inline.interfaces import IInlineKeyboardText
from src.presentation.bot.content.text_content.keyboard_content.reply.interfaces import IReplyKeyboardText


@dataclass
class IContent:
    language: Language
    text: IText
    inline: IInlineKeyboardText
    reply: IReplyKeyboardText
