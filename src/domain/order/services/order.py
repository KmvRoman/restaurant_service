from typing import Optional

from src.domain.order.constants.order import PaymentType, OrderType, OrderStatus
from src.domain.order.entities.order import PickUpOrder, ShippingOrder, Location, ProductOrder, Order
from src.domain.user.entities.user import UserId


class OrderService:
    max_kilometers_for_fixed_shipping_amount = 1
    fixed_shipping_amount = 10000
    shipping_price_per_kilometer = 1250

    def create_order(
            self, user_id: UserId, payment_type: PaymentType, phone: str, order_type: OrderType,
            products: list[ProductOrder], location: Optional[Location],
            address: Optional[str], comment: Optional[str], shipping_length: Optional[float],
    ) -> ShippingOrder | PickUpOrder:
        if order_type == OrderType.shipping:
            return ShippingOrder(
                id=None, user_id=user_id, phone=phone, payment_type=payment_type,
                order_type=order_type, products=products,
                amount=self.calculate_amount(products=products), status=OrderStatus.waiting, location=location,
                address=address, comment=comment, shipping_length=shipping_length,
                total_amount=self.calculate_total_amount(products=products, shipping_length=shipping_length),
            )
        else:
            return PickUpOrder(
                id=None, user_id=user_id, phone=phone, payment_type=payment_type,
                order_type=order_type, products=products, amount=self.calculate_amount(products=products),
                status=OrderStatus.waiting, total_amount=self.calculate_amount(products=products),
            )

    def calculate_amount(self, products: list[ProductOrder]) -> int:
        amount = 0
        for pr in products:
            amount += pr.price * pr.count
        return amount

    def calculate_total_amount(self, products: list[ProductOrder], shipping_length: Optional[float]) -> int | None:
        return (
                self.calculate_amount(products=products) +
                self.calculate_shipping_amount(shipping_length=shipping_length)
        )

    def calculate_shipping_amount(self, shipping_length: Optional[float]) -> int:
        shipping_length = shipping_length
        if shipping_length is None:
            return 0
        elif shipping_length <= self.max_kilometers_for_fixed_shipping_amount:
            return self.fixed_shipping_amount
        else:
            return int(
                (
                        shipping_length - self.max_kilometers_for_fixed_shipping_amount
                ) * self.shipping_price_per_kilometer
            ) + self.fixed_shipping_amount

    def accept_order(self, order: Order) -> Order:
        order.status = OrderStatus.accepted
        return order

    def choose_payment_method(self, order: Order, payment_type: PaymentType) -> Order:
        order.payment_type = payment_type
        return order
