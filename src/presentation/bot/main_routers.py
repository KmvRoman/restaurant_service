from src.presentation.bot.handlers.admin import admin_router
from src.presentation.bot.handlers.user import user_router

routers = [
    user_router, admin_router
]
