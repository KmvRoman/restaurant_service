from aiogram import Router

from .pickup import pickup
from .shipping import shipping

order = Router()
order.include_routers(shipping, pickup)
