from src.domain.user.constants.user import Language
from src.presentation.bot.content.fasade.interfaces import IContent
from src.presentation.bot.content.fasade.ru import ContentRu
from src.presentation.bot.content.fasade.uz import ContentUz
from src.presentation.bot.content.text_content.keyboard_content.inline.ru import RussianInlineKeyboardText
from src.presentation.bot.content.text_content.keyboard_content.inline.uz import UzbekInlineKeyboardText
from src.presentation.bot.content.text_content.keyboard_content.reply.ru import RussianReplyKeyboardText
from src.presentation.bot.content.text_content.keyboard_content.reply.uz import UzbekReplyKeyboardText
from src.presentation.bot.content.text_content.ru import RussianText
from src.presentation.bot.content.text_content.uz import UzbekText


class LanguageManager:
    def __init__(self, implements: list[IContent]):
        self.implements = implements

    def __call__(self, language: Language) -> IContent | None:
        for instance in self.implements:
            if instance.language == language:
                return instance
        raise NotImplementedError()


if __name__ == '__main__':
    content = [
        ContentRu(
            text=RussianText(),
            inline=RussianInlineKeyboardText(user_repo=None, inline_keyboard=None),
            reply=RussianReplyKeyboardText(reply_keyboard=None),
        ),
        ContentUz(
            text=UzbekText(),
            inline=UzbekInlineKeyboardText(user_repo=None, inline_keyboard=None),
            reply=UzbekReplyKeyboardText(reply_keyboard=None),
        )
    ]
    language_manager = LanguageManager()
    c = language_manager(language=Language.uz, implements=content)
