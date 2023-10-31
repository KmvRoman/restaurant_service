from aiogram.fsm.context import FSMContext

from src.application.create_order.dto import CreateOrderDtoInput
from src.domain.order.entities.order import ProductOrder, OrderId
from src.domain.user.entities.user import User
from src.infrastructure.ioc.interfaces import InteractorFactory
from src.presentation.bot.states.state_data.order import PickupData, ShippingData


async def create_order_pickup(
        ioc: InteractorFactory, user: User, order: PickupData,
) -> OrderId:
    create_order_case = await ioc.create_order()
    create_order = await create_order_case(data=CreateOrderDtoInput(
        restaurant_location_id=order.restaurant_location_id, user_id=user.id,
        phone=order.phone, order_type=order.order_type,
        products=[
            ProductOrder(
                product_id=i.product_id, modification=i.modification,
                count=i.count, price=i.price
            ) for i in order.products
        ], location=None, address=None, comment=None, shipping_length=None,
    ))
    return create_order.order_id


async def create_order_shipping(
        ioc: InteractorFactory, user: User, order: ShippingData,
) -> OrderId:
    create_order_case = await ioc.create_order()
    create_order = await create_order_case(data=CreateOrderDtoInput(
        restaurant_location_id=order.restaurant_location_id, user_id=user.id,
        phone=order.phone, order_type=order.order_type,
        products=[
            ProductOrder(
                product_id=i.product_id, modification=i.modification,
                count=i.count, price=i.price
            ) for i in order.products
        ], location=order.location, address=order.address, comment=order.comment,
        shipping_length=order.shipping_length,
    ))
    return create_order.order_id
