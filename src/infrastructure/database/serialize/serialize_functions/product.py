from src.domain.order.constants.basket import BasketStatus
from src.domain.order.constants.order import OrderType
from src.domain.order.entities.basket import Basket, ProductBasket
from src.domain.order.entities.basket_view import BasketViewInput, PreparedProductInput
from src.domain.product.constants.product import ProductMode, ProductStatus
from src.domain.product.entities.product import Product, ProductName, ProductDescription, ProductPrice, \
    ProductPriceName, ProductId
from src.domain.product.entities.product_view import ProductView, Price, ProductsCategory, AdminProductsView, \
    ProductAdmin, AdminProductPrice
from src.domain.restaurant.constants.constants import MenuProductStatus
from src.domain.user.entities.user import UserId
from src.infrastructure.database.serialize.models.product import ShowProduct, ShowBasket, ViewBasket, \
    ShowProductsAdminMenu, ShowFullProduct, ShowCoreProduct


def serialize_products(payload: list[tuple]) -> list[ProductView]:
    category_products: list[ProductView] = []
    for pr in payload:
        product_row = ShowProduct(*pr)
        category = ProductView(id=product_row.category_id, category=product_row.category_name, products=[])
        if category not in category_products:
            category_products.append(category)
    for pr in payload:
        product_row = ShowProduct(*pr)
        for cat in category_products:
            product = ProductsCategory(
                menu_product_id=product_row.menu_product_id, product_id=product_row.product_id,
                photo=product_row.photo, name=product_row.name, description=product_row.description,
                mode=product_row.mode,
                price=[],
                product_status=product_row.product_status,
                menu_product_status=product_row.menu_product_status,
            )
            if cat.id == product_row.category_id and product not in cat.products:
                cat.products.append(product)
    for pr in payload:
        product_row = ShowProduct(*pr)
        for cat in category_products:
            for prod in cat.products:
                price = Price(id=product_row.price_id, name=product_row.price_name, price=product_row.price)
                if prod.product_id == product_row.product_id and price not in prod.price:
                    prod.price.append(price)
    return category_products


def serialize_basket(payload: list[tuple]) -> Basket:
    user_id: UserId | None = None
    prepared: list[ProductBasket] = []
    status: BasketStatus | None = None
    for bas in payload:
        basket_row = ShowBasket(*bas)
        if user_id is None or status is None:
            user_id = basket_row.user_id
            status = basket_row.status
        if basket_row.product_id is None and basket_row.count is None:
            break
        product = ProductBasket(
            product_id=basket_row.product_id, count=basket_row.count,
            modification=basket_row.modification,
        )
        if product not in prepared:
            prepared.append(product)
    return Basket(user_id=user_id, prepared=prepared, status=status)


def serialize_basket_view(payload: list[tuple]) -> BasketViewInput:
    user_id: UserId | None = None
    prepared: list[PreparedProductInput] = []
    for bas in payload:
        basket_row = ViewBasket(*bas)
        if user_id is None:
            user_id = basket_row.user_id
        if basket_row.product_id is None and basket_row.count is None:
            break
        product = PreparedProductInput(
            product_id=basket_row.product_id, photo=basket_row.photo,
            modification=basket_row.modification, product_name=basket_row.name,
            price_name=basket_row.price_name, count=basket_row.count, price=basket_row.price,
        )
        if product not in prepared:
            prepared.append(product)
    return BasketViewInput(user_id=user_id, prepared=prepared)


def serialize_admin_category_products(payload: tuple) -> list[AdminProductsView]:
    products = []
    for pr in payload:
        product = ShowProductsAdminMenu(*pr)
        products.append(AdminProductsView(
            category_name=product.category_name,
            menu_product_id=product.menu_product_id, name=product.name,
            menu_product_status=product.menu_product_status,
        ))
    return products


def show_product_admin(payload: list) -> ProductAdmin:
    id: int | None = None
    photo: str | None = None
    name: list[ProductName] | list = []
    description: list[ProductDescription] | list = []
    mode: ProductMode | None = None
    price: list[AdminProductPrice] | list = []
    product_status: ProductStatus | None = None
    menu_product_status: MenuProductStatus | None = None
    for pr in payload:
        product_row = ShowFullProduct(*pr)
        if id is None:
            id = product_row.id
            photo = product_row.photo
            mode = product_row.mode
            product_status = product_row.product_status
            menu_product_status = product_row.menu_product_status
        if ProductName(name=product_row.name, language=product_row.name_language) not in name:
            name.append(ProductName(name=product_row.name, language=product_row.name_language))
        if product_row.description is not None and ProductDescription(
                description=product_row.description,
                language=product_row.description_language
        ) not in description:
            description.append(ProductDescription(
                description=product_row.description,
                language=product_row.description_language
            ))
        if product_row.price_id in [i.id for i in price]:
            for pc in price:
                if pc.id == product_row.price_id:
                    price_name = ProductPriceName(
                            name=product_row.price_name,
                            language=product_row.price_name_language,
                        )
                    if price_name not in pc.name:
                        pc.name.append(
                            ProductPriceName(
                                name=product_row.price_name,
                                language=product_row.price_name_language,
                            )
                        )
        else:
            price.append(AdminProductPrice(
                id=product_row.price_id, name=[
                    ProductPriceName(name=product_row.price_name, language=product_row.price_name_language),
                ],
                price=product_row.price,
            )
            )
    return ProductAdmin(
        id=id, photo=photo, name=name, description=description, mode=mode,
        price=price, product_status=product_status, menu_product_status=menu_product_status,
    )


def show_product_core(payload: list) -> Product:
    id: ProductId | None = None
    photo: str | None = None
    name: list[ProductName] | list = []
    description: list[ProductDescription] | list = []
    mode: ProductMode | None = None
    price: list[AdminProductPrice] | list = []
    product_status: ProductStatus | None = None
    for pr in payload:
        product_row = ShowCoreProduct(*pr)
        if id is None:
            id = product_row.id
            photo = product_row.photo
            mode = product_row.mode
            product_status = product_row.product_status
        if ProductName(name=product_row.name, language=product_row.name_language) not in name:
            name.append(ProductName(name=product_row.name, language=product_row.name_language))
        if product_row.description is not None and ProductDescription(
                description=product_row.description,
                language=product_row.description_language
        ) not in description:
            description.append(ProductDescription(
                description=product_row.description,
                language=product_row.description_language
            ))
        if product_row.price_id in [i.id for i in price]:
            for pc in price:
                if pc.id == product_row.price_id:
                    price_name = ProductPriceName(
                            name=product_row.price_name,
                            language=product_row.price_name_language,
                        )
                    if price_name not in pc.name:
                        pc.name.append(
                            ProductPriceName(
                                name=product_row.price_name,
                                language=product_row.price_name_language,
                            )
                        )
        else:
            price.append(AdminProductPrice(
                id=product_row.price_id, name=[
                    ProductPriceName(name=product_row.price_name, language=product_row.price_name_language),
                ],
                price=product_row.price,
            )
            )
    return Product(
        id=id, photo=photo, name=name, description=description, mode=mode,
        price=price, status=product_status,
    )
