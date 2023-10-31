from aiohttp import ClientSession

from src.domain.order.entities.order import Location
from src.infrastructure.exceptions.exceptions import AddressError
from src.infrastructure.web.get_address_from_location.models import Results


class GetAddressFromLocation:
    def __init__(self, apikey: str, format: str, lang: str):
        self.apikey = apikey
        self.format = format
        self.lang = lang

    async def get_address(self, location: Location) -> str:
        async with ClientSession() as session:
            response = await session.get(
                url="https://geocode-maps.yandex.ru/1.x?",
                params={
                    "apikey": self.apikey,
                    "geocode": f"{location.longitude}, {location.latitude}",
                    "format": self.format,
                    "lang": self.lang, "results": 10,
                })
            json_data = await response.json()
            if len(json_data["response"]["GeoObjectCollection"]["featureMember"]) == 0:
                raise AddressError
            return [
                Results(**i) for i in json_data["response"]["GeoObjectCollection"]["featureMember"]
            ][0].GeoObject.metaDataProperty.GeocoderMetaData.Address.formatted
