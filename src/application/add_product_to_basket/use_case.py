from src.application.add_product_to_basket.dto import AddProductToBasketDtoInput
from src.application.add_product_to_basket.interfaces import DbGateway
from src.application.common.use_case import UseCase
from src.domain.order.entities.basket import ProductBasket
from src.domain.order.services.basket import BasketService


class AddProductToBasketCase(UseCase[AddProductToBasketDtoInput, None]):
    def __init__(self, db_gateway: DbGateway, basket_service: BasketService):
        self.db_gateway = db_gateway
        self.basket_service = basket_service

    async def __call__(self, data: AddProductToBasketDtoInput) -> None:
        basket = await self.db_gateway.get_basket_by_user_id(user_id=data.user_id)
        product = ProductBasket(product_id=data.product_id, count=data.count, modification=data.modification)
        if basket is None:
            basket = self.basket_service.create_basket(user_id=data.user_id, prepared=[])
            self.basket_service.add_product(product=product, basket=basket)
            await self.db_gateway.create_basket(basket=basket)
        else:
            self.basket_service.add_product(product=product, basket=basket)
            await self.db_gateway.update_product_basket(product_basket=basket.prepared, user_id=basket.user_id)
        await self.db_gateway.commit()
