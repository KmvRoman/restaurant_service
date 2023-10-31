from datetime import timedelta

from redis.asyncio import Redis

from src.infrastructure.cache.models import InsertRedisData


class RedisConnect:
    def __init__(self, host: str, port: int, db: int, password: str):
        self.host = host
        self.port = port
        self.db = db
        self.password = password

    def __call__(self) -> Redis:
        return Redis(
            host=self.host, port=self.port, db=self.db,
            password=self.password,
        )


class RedisCacheSystem:
    def __init__(self, redis: Redis):
        self.redis = redis

    async def set_common(self, payload: InsertRedisData):
        await self.redis.set(
            name=payload.name, value=payload.value,
            ex=timedelta(seconds=payload.expires),
        )

    async def get_common(self, name: str) -> str | None:
        data = (await self.redis.get(name=name))
        if data is None:
            return
        return data.decode()

    async def compare_data_common(self, payload: InsertRedisData) -> bool:
        value = await self.get_common(name=payload.name)
        if value:
            if value == payload.value:
                return True
            return False
        return False

    async def set(self, payload: InsertRedisData, user_id: int):
        await self.redis.set(
            name=f"{payload.name}_{user_id}", value=payload.value,
            ex=timedelta(seconds=payload.expires),
        )

    async def get(self, name: str, user_id: int) -> str | None:
        data = (await self.redis.get(name=f"{name}_{user_id}"))
        if data is None:
            return
        return data.decode()

    async def compare_data(self, payload: InsertRedisData, user_id: int) -> bool:
        value = await self.get(name=payload.name, user_id=user_id)
        if value:
            if value == payload.value:
                return True
            return False
        return False
