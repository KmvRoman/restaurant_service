from src.presentation.bot.handlers.admin import admin_router
from src.presentation.bot.handlers.errors import error_catcher
from src.presentation.bot.handlers.user import user_router

routers = [
    user_router, admin_router, error_catcher,
]
