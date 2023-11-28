from src.domain.order.entities.order import Location
from src.domain.order.entities.order_view import ReadOrderAdmin, ReadAdminOrderProduct, ReadOrderUser, \
    ReadUserOrderProduct
from src.infrastructure.database.serialize.models.order import AdminOrderShow, AdminProductShow, UserOrderShow, \
    UserProductShow


def serialize_admin_order(payload: tuple) -> ReadOrderAdmin:
    payload_row = AdminOrderShow(*payload)
    if payload_row.total_amount is None:
        return ReadOrderAdmin(
            order_id=payload_row.order_id, products=[], name=payload_row.name, phone=payload_row.phone,
            payment_type=payload_row.payment_type, address=None, comment=None,
            location=None,
            shipping_amount=payload_row.amount, total_cost=payload_row.amount,
        )
    else:
        return ReadOrderAdmin(
            order_id=payload_row.order_id, products=[], name=payload_row.name, phone=payload_row.phone,
            payment_type=payload_row.payment_type, address=payload_row.address, comment=payload_row.comment,
            location=Location(longitude=payload_row.longitude, latitude=payload_row.latitude),
            shipping_amount=payload_row.total_amount - payload_row.amount, total_cost=payload_row.total_amount,
        )


def serialize_admin_product(payload: list[tuple]) -> list[ReadAdminOrderProduct]:
    response: list[ReadAdminOrderProduct] = []
    for i in payload:
        payload_row = AdminProductShow(*i)
        response.append(ReadAdminOrderProduct(
            name=payload_row.name, price_name=payload_row.price_name, count=payload_row.count,
        ))
    return response


def serialize_user_order(payload: tuple) -> ReadOrderUser:
    payload_row = UserOrderShow(*payload)
    if payload_row.total_amount is None:
        return ReadOrderUser(
            order_id=payload_row.order_id, products=[],
            amount=None, total_cost=payload_row.amount,
        )
    else:
        return ReadOrderUser(
            order_id=payload_row.order_id, products=[],
            amount=payload_row.amount, total_cost=payload_row.total_amount,
        )


def serialize_user_product(payload: list[tuple]) -> list[ReadUserOrderProduct]:
    response: list[ReadUserOrderProduct] = []
    for i in payload:
        payload_row = UserProductShow(*i)
        response.append(ReadUserOrderProduct(
            name=payload_row.name, price_name=payload_row.price_name,
            price=payload_row.price, count=payload_row.count,
            total_price=payload_row.price * payload_row.count,
        ))
    return response
