from src.presentation.bot.content.content_enums import ExistingTypes
from src.presentation.bot.content.text_content.interfaces import IFormat


class FormatManager:

    def __init__(self, formatters: list[IFormat]):
        self.formatters = formatters

    def __call__(self, type: ExistingTypes) -> IFormat:
        for frmt in self.formatters:
            if frmt.format == type:
                return frmt
        raise NotImplementedError()
