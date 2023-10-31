from aiohttp import ClientSession
from pydantic import BaseModel

from src.application.common.interfaces import ShippingLength
from src.domain.order.entities.order import Location
from src.infrastructure.cache.models import InsertRedisData
from src.infrastructure.cache.redis_cache import RedisCacheSystem
from src.infrastructure.exceptions.exceptions import WrongLocations


class ShippingLengthInfo(BaseModel):
    length: int


class ShippingLengthImpl(ShippingLength):
    key_started = "shipping_length"

    def __init__(self, redis_cache: RedisCacheSystem):
        self.redis_cache = redis_cache

    async def calculate_shipping_length(self, user_location: Location, restaurant_location: Location) -> int:
        async with ClientSession() as session:
            response = await session.get(url=(
                f"https://cubinc.uz/maps/route?"
                f"longitude_a={user_location.longitude}&latitude_a={user_location.latitude}&"
                f"longitude_b={restaurant_location.longitude}&latitude_b={restaurant_location.latitude}"
            )
            )
            try:
                return int(round((await response.json())["distance"]))
            except KeyError:
                raise WrongLocations

    async def get_shipping_length(self, user_location: Location, restaurant_location: Location) -> int:
        shipping_length = await self.redis_cache.get_common(
            name=f"{self.key_started}-{user_location.longitude}|{user_location.latitude}-"
                 f"{restaurant_location.longitude}|{restaurant_location.latitude}",
        )
        if shipping_length is None:
            length = await self.calculate_shipping_length(
                user_location=user_location, restaurant_location=restaurant_location,
            )
            await self.redis_cache.set_common(payload=InsertRedisData(
                name=f"{self.key_started}-{user_location.longitude}|{user_location.latitude}-"
                     f"{restaurant_location.longitude}|{restaurant_location.latitude}",
                value=ShippingLengthInfo(length=length).model_dump_json(),
                expires=86400,
            ))
        shipping_length = await self.redis_cache.get_common(
            name=f"{self.key_started}-{user_location.longitude}|{user_location.latitude}-"
                 f"{restaurant_location.longitude}|{restaurant_location.latitude}",
        )
        return ShippingLengthInfo.model_validate_json(shipping_length).length
