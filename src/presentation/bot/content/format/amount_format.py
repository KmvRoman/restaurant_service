from src.presentation.bot.content.content_enums import ExistingTypes
from src.presentation.bot.content.text_content.interfaces import IFormat


class FormatAmount(IFormat):
    format = ExistingTypes.Amount

    def parse_unit_of_format_type(self, obj: int) -> str:
        return "{0:,}".format(obj).replace(",", " ")
