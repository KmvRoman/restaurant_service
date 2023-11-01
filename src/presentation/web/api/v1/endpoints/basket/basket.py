from fastapi import APIRouter, Depends

from src.application.add_product_to_basket.dto import AddProductToBasketDtoInput
from src.application.common.exceptions import CurrentBasketNotFound, RestaurantLocationsNotFound, ProductsIsEmpty
from src.application.delete_product_from_basket.dto import DeleteProductFromBasketDtoInput
from src.application.read_current_basket.dto import ReadCurrentBasketDtoInput
from src.application.read_products.dto import ReadProductsDtoInput
from src.domain.restaurant.entities.restaurant_view import RestaurantId
from src.infrastructure.database.repositories.user_repository import UserRepository
from src.infrastructure.exceptions.exceptions import WrongLocations
from src.infrastructure.ioc.interfaces import InteractorFactory
from src.presentation.web.api.v1.dependencies.dependencies import IocDependencyMarker, UserRepositoryDependencyMarker
from src.presentation.web.api.v1.dto.basket.request import (
    GetProductsRequest, AddProductRequest, DeleteProductRequest, GetBasketRequest,
)
from src.presentation.web.api.v1.dto.basket.response import (
    SuccessResponse, GetBasketResponse, PreparedProducts,
    ProductPrice, CategoryProducts, ProductsPerCategory, GetBannersResponse,
)
from src.presentation.web.exceptions.application.basket import BasketIsEmpty, LocationsInvalid

basket_router = APIRouter(prefix="/api/v1/basket", tags=["Basket"])


@basket_router.post(path="/add")
async def add_product(
        payload: AddProductRequest,
        interactor: InteractorFactory = Depends(IocDependencyMarker),
) -> SuccessResponse:
    add_product_case = await interactor.add_product_to_basket()
    await add_product_case(
        data=AddProductToBasketDtoInput(
            user_id=payload.user_id, product_id=payload.product_id,
            count=payload.count, modification=payload.modification,
        )
    )
    return SuccessResponse()


@basket_router.post(path="/remove")
async def remove_product(
        payload: DeleteProductRequest,
        interactor: InteractorFactory = Depends(IocDependencyMarker),
) -> SuccessResponse:
    delete_product_case = await interactor.delete_product_from_basket()
    try:
        await delete_product_case(
            data=DeleteProductFromBasketDtoInput(
                user_id=payload.user_id, product_id=payload.product_id,
                modification=payload.modification,
            )
        )
    except ProductsIsEmpty:
        raise BasketIsEmpty
    return SuccessResponse()


@basket_router.post(path="/products", response_model_exclude_none=True)
async def get_products(
        payload: GetProductsRequest,
        interactor: InteractorFactory = Depends(IocDependencyMarker),
) -> list[CategoryProducts]:
    products_get = await interactor.read_products()
    try:
        products = await products_get(
            data=ReadProductsDtoInput(
                restaurant_id=payload.restaurant_id, user_location=payload.user_location,
                language=payload.language,
            )
        )
    except RestaurantLocationsNotFound:
        raise LocationsInvalid
    return [
        CategoryProducts(
            id=pr.id, category=pr.category,
            products=[ProductsPerCategory(
                menu_product_id=prod.menu_product_id, product_id=prod.product_id, photo=prod.photo,
                name=prod.name, description=prod.description, mode=prod.mode, price=[
                    ProductPrice(id=price.id, name=price.name, price=price.price) for price in prod.price
                ],
                product_status=prod.product_status, menu_product_status=prod.menu_product_status,
            ) for prod in pr.products]
        ) for pr in products
    ]


@basket_router.post(path="/current", response_model_exclude_none=True)
async def get_basket(
        payload: GetBasketRequest,
        interactor: InteractorFactory = Depends(IocDependencyMarker),
) -> GetBasketResponse:
    basket_view = await interactor.read_current_basket()
    try:
        basket = await basket_view(data=ReadCurrentBasketDtoInput(
            user_id=payload.user_id, user_location=payload.user_location,
            restaurant_location_id=payload.restaurant_location_id,
            order_type=payload.order_type, language=payload.language,
        ))
    except CurrentBasketNotFound:
        return GetBasketResponse(
            user_id=payload.user_id, order_type=payload.order_type, amount=0,
            shipping_amount=None, total_amount=0,
            products=[],
        )
    except WrongLocations:
        raise LocationsInvalid
    return GetBasketResponse(
        user_id=basket.user_id, order_type=basket.order_type, amount=basket.amount,
        shipping_amount=basket.shipping_amount, total_amount=basket.total_amount,
        products=[PreparedProducts(
            product_id=pr.product_id, photo=pr.photo, name=pr.name,
            modification=pr.modification, price_name=pr.price_name,
            count=pr.count, price=pr.price, amount=pr.amount,
        ) for pr in basket.prepared]
    )


@basket_router.get(path="/banner")
async def get_banners(
        restaurant_id: RestaurantId,
        user_repo: UserRepository = Depends(UserRepositoryDependencyMarker),
) -> GetBannersResponse:
    banners = await user_repo.get_banners(restaurant_id=restaurant_id)
    return GetBannersResponse(banners=banners)
