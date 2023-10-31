from src.application.common.exceptions import ProductsIsEmpty
from src.application.common.use_case import UseCase
from src.application.delete_product_from_basket.dto import DeleteProductFromBasketDtoInput
from src.application.delete_product_from_basket.interfaces import DbGateway
from src.domain.order.services.basket import BasketService


class DeleteProductFromBasketCase(UseCase[DeleteProductFromBasketDtoInput, None]):
    def __init__(self, db_gateway: DbGateway, basket_service: BasketService):
        self.db_gateway = db_gateway
        self.basket_service = basket_service

    async def __call__(self, data: DeleteProductFromBasketDtoInput) -> None:
        basket = await self.db_gateway.get_basket_by_user_id(user_id=data.user_id)
        if basket is None:
            raise ProductsIsEmpty
        self.basket_service.delete_product(
            product_id=data.product_id, modification=data.modification,
            basket=basket,
        )
        await self.db_gateway.update_product_basket(product_basket=basket.prepared, user_id=basket.user_id)
        await self.db_gateway.commit()
