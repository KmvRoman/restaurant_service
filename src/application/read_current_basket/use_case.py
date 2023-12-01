from src.application.common.exceptions import CurrentBasketNotFound
from src.application.common.use_case import UseCase
from src.application.read_current_basket.dto import ReadCurrentBasketDtoInput, ReadCurrentBasketDtoOutput, \
    PreparedBasketProduct
from src.application.read_current_basket.interfaces import DbGateway, ShippingLengthCalculateService
from src.domain.order.services.basket_view import BasketViewService
from src.domain.order.services.order import OrderService


class ReadCurrentBasketCase(UseCase[ReadCurrentBasketDtoInput, ReadCurrentBasketDtoOutput]):
    def __init__(
            self, db_gateway: DbGateway, basket_view_service: BasketViewService,
            shipping_length: ShippingLengthCalculateService, order_service: OrderService,
    ):
        self.db_gateway = db_gateway
        self.basket_view_service = basket_view_service
        self.shipping_length_calculate_service = shipping_length
        self.order_service = order_service

    async def __call__(self, data: ReadCurrentBasketDtoInput) -> ReadCurrentBasketDtoOutput:
        basket = await self.db_gateway.read_current_basket(user_id=data.user_id, language=data.language)
        if basket is None:
            raise CurrentBasketNotFound
        restaurant_location = await self.db_gateway.read_restaurant_location(
            location_id=data.restaurant_location_id)
        if data.user_location is None:
            shipping_amount = None
            shipping_length = None
        else:
            shipping_length = await self.shipping_length_calculate_service.get_shipping_length(
                user_location=data.user_location, restaurant_location=restaurant_location,
            )
            shipping_amount = self.order_service.calculate_shipping_amount(shipping_length=shipping_length)
        basket_view = self.basket_view_service.current_basket(
            basket=basket, shipping_amount=shipping_amount, shipping_length=shipping_length, order_type=data.order_type,
        )
        return ReadCurrentBasketDtoOutput(
            user_id=basket_view.user_id, prepared=[
                PreparedBasketProduct(
                    product_id=pr.product_id, photo=pr.photo, name=pr.name,
                    modification=pr.modification,
                    price_name=pr.price_name, count=pr.count, price=pr.price,
                    amount=pr.amount
                ) for pr in basket_view.prepared
            ],
            order_type=basket_view.order_type, amount=basket_view.amount,
            shipping_amount=basket_view.shipping_amount, shipping_length=basket_view.shipping_length,
            total_amount=basket_view.total_amount,
        )
