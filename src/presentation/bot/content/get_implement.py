from src.domain.user.constants.user import Language
from src.presentation.bot.content.fasade.interfaces import IContent


class LanguageManager:
    def __init__(self, implements: list[IContent]):
        self.implements = implements

    def __call__(self, language: Language) -> IContent | None:
        for instance in self.implements:
            if instance.language == language:
                return instance
        raise NotImplementedError()
