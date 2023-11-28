from src.domain.order.constants.order import OrderType
from src.domain.order.entities.basket_view import BasketViewInput, BasketViewOutput, PreparedProductOutput


class BasketViewService:
    def current_basket(
            self, basket: BasketViewInput, shipping_amount: int | None,
            order_type: OrderType,
    ) -> BasketViewOutput:
        prepared = []
        amount = 0
        for pr in basket.prepared:
            prepared.append(PreparedProductOutput(
                product_id=pr.product_id,
                photo=pr.photo,
                name=pr.product_name,
                modification=pr.modification,
                price_name=pr.price_name,
                count=pr.count,
                price=pr.price,
                amount=pr.count * pr.price,
            )
            )
            amount += pr.count * pr.price
        return BasketViewOutput(
            user_id=basket.user_id, prepared=prepared, order_type=order_type,
            amount=amount, shipping_amount=shipping_amount,
            total_amount=amount + (0 if shipping_amount is None else shipping_amount),
        )
