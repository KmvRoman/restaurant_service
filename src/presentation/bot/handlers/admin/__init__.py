from aiogram import Router

from .menu import admin
from .product.product import product_router
from .product.stop_list import stop_router

admin_router = Router(name="Administrator")
admin_router.include_routers(admin, product_router, stop_router)

