from src.api.v1.endpoints.dto.order.request import TimePeriod
from src.content.content_enums import ExistingTypes
from src.content.interfaces import IFormat


class FormatTimePeriod(IFormat):
    format = ExistingTypes.TimePeriod

    def parse_list_of_format_type(self, obj: list[TimePeriod]) -> str:
        string = ""
        for t in obj:
            string += f"{t.time_from.isoformat()[:5]} - {t.time_until.isoformat()[:5]}, "
        else:
            string = string[:-2]
        return string

    def parse_unit_of_format_type(self, obj: TimePeriod) -> str:
        return (
            f"{obj.time_from.isoformat()[:5]} - {obj.time_until.isoformat()[:5]}"
        )
