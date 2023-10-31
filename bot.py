import asyncio

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from src.infrastructure.cache.redis_cache import RedisConnect, RedisCacheSystem
from src.infrastructure.config.parse_config import load_config, BASE_DIR
from src.infrastructure.database.repositories.user_repository import UserRepository
from src.infrastructure.ioc.ioc import IoC
from src.infrastructure.web.s3.client import S3Client
from src.presentation.bot.content.initialize_content_factory import initialize_content
from src.presentation.bot.filters.create_user_filter import CreateUserFilter
from src.presentation.bot.filters.current_restaurant import CurrentRestaurant
from src.presentation.bot.main_routers import routers


async def main():
    config = load_config(BASE_DIR / "infrastructure" / "config" / "config.yaml")
    bot = Bot(token=config.tg_bot.token, parse_mode=ParseMode.HTML)
    r = Redis(
        host=config.redis.host, port=config.redis.port,
        password=config.redis.password, db=config.redis.db,
    )
    if config.tg_bot.use_redis:
        storage = RedisStorage(redis=r)
    else:
        storage = MemoryStorage()
    engine = create_async_engine(url=config.database.connection_uri)
    session_make = sessionmaker(  # NOQA
        engine, class_=AsyncSession, expire_on_commit=False, autoflush=False
    )
    redis_connect = RedisConnect(
        host=config.redis.host, port=config.redis.port,
        password=config.redis.password, db=config.redis.db,
    )
    get_connect = redis_connect()
    redis = RedisCacheSystem(redis=get_connect)

    user_repo = UserRepository(session_or_pool=session_make)
    ioc = IoC(db_gateway=user_repo, redis_cache=redis, config=config)
    content = initialize_content(user_repo=user_repo)
    s3 = S3Client(
        aws_access_key_id=config.s3.aws_access_key_id,
        aws_secret_access_key=config.s3.aws_secret_access_key,
        service_name=config.s3.service_name, bucket=config.s3.bucket, path=config.s3.path,
        location=config.s3.location,
    )
    dp = Dispatcher(
        storage=storage, ioc=ioc, user_repo=user_repo, content=content, s3=s3,
    )

    await bot.set_my_commands(commands=[
        BotCommand(
            command="start",
            description="tap to start",
        ), BotCommand(
            command="admin",
            description="tap to admin",
        ),
        BotCommand(
            command="st",
            description="command description",
        ),
    ])

    dp.message.filter(CreateUserFilter(), CurrentRestaurant())
    dp.callback_query.filter(CreateUserFilter(), CurrentRestaurant())
    dp.startup.register(start_bot)
    dp.shutdown.register(shutdown_bot)
    dp.include_routers(*routers)
    await bot.delete_webhook(drop_pending_updates=True)
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()
        session_make.close_all()
        await engine.dispose()
        await get_connect.close()


async def start_bot():
    print("Bot started!")


async def shutdown_bot():
    print("Bot shutdown!")


def cli():
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, AttributeError):
        print("KeyboardInterrupt")


if __name__ == '__main__':
    cli()
