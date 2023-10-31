from typing import Optional

from src.domain.order.constants.basket import BasketStatus
from src.domain.order.entities.basket import Basket, ProductBasket
from src.domain.product.entities.product import ProductId
from src.domain.user.entities.user import UserId


class BasketService:
    def create_basket(self, user_id: UserId, prepared: list[ProductBasket]) -> Basket:
        return Basket(user_id=user_id, prepared=prepared, status=BasketStatus.prepare)

    def add_product(self, product: ProductBasket, basket: Basket) -> Basket:
        for pr in basket.prepared:
            if product.modification is None:
                if pr.product_id == product.product_id:
                    pr.count += product.count
                    break
            else:
                if pr.product_id == product.product_id and pr.modification == product.modification:
                    pr.count += product.count
                    break
        else:
            basket.prepared.append(product)
        return basket

    def delete_product(self, product_id: ProductId, modification: Optional[int], basket: Basket) -> Basket:
        for count, pr in enumerate(basket.prepared):
            if pr.product_id == product_id and pr.modification == modification:
                basket.prepared.pop(count)
                break
        return basket
