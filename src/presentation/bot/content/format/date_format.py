from datetime import datetime, date

from src.content.content_enums import ExistingTypes
from src.content.interfaces import IFormat


class FormatDateTime(IFormat):
    format = ExistingTypes.DateTime

    def parse_list_of_format_type(self, obj: list[date | datetime]) -> str:
        pass

    def parse_unit_of_format_type(self, obj: date | datetime) -> str:
        if isinstance(obj, str):
            return obj
        if isinstance(obj, datetime):
            return datetime.strftime(obj, "%d.%m.%Y")
        elif isinstance(obj, date):
            return datetime.strftime(obj, "%d.%m.%Y")
        return obj
