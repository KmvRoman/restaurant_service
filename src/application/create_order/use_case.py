from src.application.common.exceptions import RestaurantLocationNotFound
from src.application.common.use_case import UseCase
from src.application.create_order.dto import CreateOrderDtoInput, CreateOrderDtoOutput
from src.application.create_order.interfaces import DbGateway, ShippingLengthResource
from src.domain.order.entities.order import ShippingOrder
from src.domain.order.services.order import OrderService


class CreateOrderCase(UseCase[CreateOrderDtoInput, CreateOrderDtoOutput]):
    def __init__(self, db_gateway: DbGateway, order_service: OrderService):
        self.db_gateway = db_gateway
        self.order_service = order_service

    async def __call__(self, data: CreateOrderDtoInput) -> CreateOrderDtoOutput:
        restaurant_location = await self.db_gateway.read_restaurant_location(
            location_id=data.restaurant_location_id)
        if restaurant_location is None:
            raise RestaurantLocationNotFound
        order = self.order_service.create_order(
            user_id=data.user_id, phone=data.phone, payment_type=data.payment_type,
            order_type=data.order_type, products=data.products,
            location=data.location, address=data.address,
            comment=data.comment, shipping_length=data.shipping_length,
        )
        if isinstance(order, ShippingOrder):
            exist_address = await self.db_gateway.exist_user_address(address=data.address, user_id=data.user_id)
            order_id = await self.db_gateway.create_shipping_order(order=order)
            if not exist_address:
                await self.db_gateway.add_address_to_pool(order_id=order_id)
        else:
            order_id = await self.db_gateway.create_pick_up_order(order=order)
        await self.db_gateway.commit()
        return CreateOrderDtoOutput(order_id=order_id)
