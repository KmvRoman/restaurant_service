from datetime import datetime

from aiohttp import ClientSession

from src.domain.restaurant.entities.restaurant_view import RestaurantId
from src.infrastructure.web.s3.client import S3Client


async def put_file(receive_url: str, restaurant_id: RestaurantId, s3: S3Client) -> str:
    async with ClientSession() as session:
        async with session.get(receive_url) as resp:
            url = s3.s3_put_object(
                name=generate_name(restaurant_id=restaurant_id),
                body=await resp.content.read(),
            )
            return url


def generate_name(restaurant_id: RestaurantId) -> str:
    return f"file_{restaurant_id}_{datetime.utcnow().timestamp()}"
