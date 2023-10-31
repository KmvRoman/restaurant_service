from aiogram import Router

from .order import order
from .user import profile_router

user_router = Router(name="UserRouter")
user_router.include_routers(profile_router, order)
