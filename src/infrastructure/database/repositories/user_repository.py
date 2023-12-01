from sqlalchemy import select, update, case, delete, desc
from sqlalchemy.exc import IntegrityError

from src.domain.order.constants.basket import BasketStatus
from src.domain.order.constants.order import OrderStatus
from src.domain.order.entities.basket import Basket, ProductBasket
from src.domain.order.entities.basket_view import BasketViewInput
from src.domain.order.entities.order import Location, PickUpOrder, OrderId, ShippingOrder, ProductOrder, Order
from src.domain.order.entities.order_view import ReadOrderAdmin, ReadAdminOrderProduct, ReadOrderUser, \
    ReadUserOrderProduct
from src.domain.product.constants.product import ProductStatus
from src.domain.product.entities.product import ProductId, Product, ProductName, ProductDescription, ProductPrice
from src.domain.product.entities.product_view import ProductView, AdminProductsView, ProductAdmin
from src.domain.restaurant.constants.constants import MenuProductStatus
from src.domain.restaurant.entities.restaurant_view import (
    RestaurantId, RestaurantLocation, LocationId, RestaurantView,
    Category, CategoryId, ReadRestaurantBranches, MenuProduct,
)
from src.domain.restaurant.entities.stop_list_view import StopList
from src.domain.user.constants.user import Language, Member
from src.domain.user.entities.user import User, UserId
from src.infrastructure.database import (
    UserTable, TelegramUserTable, RestaurantLocationsTable, MenuProductTable,
    ProductNameTable, ProductTable, ProductImageTable, ProductDescriptionTable,
    ProductPriceTable, ProductPriceNameTable, BasketTable, ProductBasketTable,
    ProductBasketModificationTable, CategoriesTable, CategoryNameTable,
    RestaurantBannerTable, RestaurantTable, RestaurantNameDescriptionTable,
    ShippingOrderTable, OrderTable, ShippingLocationTable, ProductOrderTable,
    GroupTable, UserAddressTable,
)
from src.infrastructure.database.enums import TelegramStatus
from src.infrastructure.database.exceptions.product import (
    ModificationSelectedError, ProductNotFound, UserNotFoundDbError,
)
from src.infrastructure.database.repositories.base import BaseRepository
from src.infrastructure.database.serialize.serialize_functions.order import serialize_admin_order, \
    serialize_admin_product, serialize_user_order, serialize_user_product
from src.infrastructure.database.serialize.serialize_functions.product import (
    serialize_products, serialize_basket, serialize_basket_view,
    serialize_admin_category_products, show_product_admin, show_product_core,
)
from src.infrastructure.database.serialize.serialize_functions.restaurant import (
    serialize_restaurant_info, serialize_category,
)


class UserRepository(BaseRepository):
    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()

    async def create_user(self, user: User) -> UserId:
        user = UserTable(name=user.name, phone=user.phone, member=user.member, language=user.language)
        self.session.add(user)
        await self.session.flush()
        return user.id

    async def edit_user_name(self, name: str, user_id: UserId) -> None:
        stmt = update(UserTable).where(UserTable.id == user_id).values({UserTable.name: name})
        await self.session.execute(stmt)

    async def edit_user_phone(self, phone: str, user_id: UserId) -> None:
        stmt = update(UserTable).where(UserTable.id == user_id).values({UserTable.phone: phone})
        await self.session.execute(stmt)

    async def edit_user_language(self, language: Language, user_id: UserId) -> None:
        stmt = update(UserTable).where(UserTable.id == user_id).values({UserTable.language: language})
        await self.session.execute(stmt)

    async def promote_user(self, member: Member, user_id: UserId) -> None:
        stmt = update(UserTable).where(UserTable.id == user_id).values({UserTable.member: member})
        await self.session.execute(stmt)
        await self.session.flush()

    async def get_user_by_user_id(self, user_id: UserId) -> User | None:
        stmt = select(UserTable).where(UserTable.id == user_id)
        result = (await self.session.execute(stmt)).scalars().first()
        if result is None:
            return None
        return User(
            id=result.id, name=result.name, phone=result.phone,
            member=result.member, language=result.language,
        )

    async def get_user_by_telegram_id(self, telegram_id: int) -> User | None:
        stmt = select(UserTable).join(
            TelegramUserTable, UserTable.id == TelegramUserTable.user_id
        ).where(TelegramUserTable.telegram_id == telegram_id)
        result = (await self.session.execute(stmt)).scalars().first()
        if result is None:
            return None
        return User(
            id=result.id, name=result.name, phone=result.phone,
            language=result.language, member=result.member,
        )

    async def get_user_id_by_telegram_id(self, telegram_id: int) -> UserId:
        stmt = select(UserTable.id).join(TelegramUserTable, UserTable.id == TelegramUserTable.user_id).where(
            TelegramUserTable.telegram_id == telegram_id,
        )
        result = (await self.session.execute(stmt)).scalars().first()
        if result is None:
            return None
        return result

    async def create_telegram_user(self, user_id: UserId, telegram_id: int) -> None:
        telegram_user = TelegramUserTable(
            user_id=user_id, telegram_id=telegram_id,
            status=TelegramStatus.active,
        )
        self.session.add(instance=telegram_user)
        await self.session.commit()

    async def read_restaurant_locations(self, restaurant_id: RestaurantId) -> list[RestaurantLocation] | None:
        stmt = select(
            RestaurantLocationsTable.id, RestaurantLocationsTable.address,
            RestaurantLocationsTable.latitude, RestaurantLocationsTable.longitude,
        ).where(RestaurantLocationsTable.restaurant_id == restaurant_id)
        result = (await self.session.execute(stmt)).all()
        if len(result) == 0:
            return None
        restaurant_locations = []
        for i in result:
            restaurant_locations.append(
                RestaurantLocation(
                    id=i[0], address=i[1],
                    latitude=i[2], longitude=i[3],
                )
            )
        return restaurant_locations

    async def read_products(self, location_id: LocationId, language: Language) -> list[ProductView] | None:
        stmt = select(
            MenuProductTable.category_id, CategoryNameTable.category, MenuProductTable.id, ProductTable.id,
            ProductImageTable.image, ProductNameTable.name, ProductDescriptionTable.description,
            ProductTable.mode, ProductPriceTable.id, ProductPriceTable.price, ProductPriceNameTable.name,
            ProductTable.status, MenuProductTable.status
        ).select_from(ProductTable).join(
            MenuProductTable, ProductTable.id == MenuProductTable.product_id
        ).join(
            CategoryNameTable, MenuProductTable.category_id == CategoryNameTable.category_id
        ).outerjoin(
            ProductImageTable, ProductTable.id == ProductImageTable.product_id
        ).join(
            ProductNameTable, ProductTable.id == ProductNameTable.product_id
        ).outerjoin(
            ProductDescriptionTable, ProductTable.id == ProductDescriptionTable.product_id
        ).join(
            ProductPriceTable, ProductTable.id == ProductPriceTable.product_id
        ).outerjoin(
            ProductPriceNameTable, ProductPriceTable.id == ProductPriceNameTable.price_id
        ).where(
            MenuProductTable.location_id == location_id, ProductNameTable.language == language,
            case(
                (ProductPriceNameTable.language.is_not(None), ProductPriceNameTable.language == language),
                else_=True,
            ),
            case(
                (ProductDescriptionTable.language.is_not(None), ProductDescriptionTable.language == language),
                else_=True,
            ),
            CategoryNameTable.language == language,
        ).order_by(MenuProductTable.category_id, MenuProductTable.id, ProductPriceTable.id)
        result = (await self.session.execute(stmt)).all()
        if len(result) == 0:
            return None
        return serialize_products(payload=result)

    async def get_basket_by_user_id(self, user_id: UserId) -> Basket | None:
        stmt = select(
            BasketTable.user_id, ProductBasketTable.product_id,
            ProductBasketTable.count, ProductBasketModificationTable.modification,
            BasketTable.status,
        ).select_from(BasketTable).outerjoin(
            ProductBasketTable, BasketTable.id == ProductBasketTable.basket_id
        ).outerjoin(
            ProductBasketModificationTable, ProductBasketTable.id == ProductBasketModificationTable.product_basket_id
        ).where(BasketTable.user_id == user_id)
        result = (await self.session.execute(stmt)).all()
        if len(result) == 0:
            return None
        return serialize_basket(payload=result)

    async def create_basket(self, basket: Basket) -> None:
        basket_create = BasketTable(user_id=basket.user_id, status=basket.status)
        self.session.add(basket_create)
        try:
            await self.session.flush()
        except IntegrityError:
            await self.session.rollback()
            raise UserNotFoundDbError(basket.user_id)
        for pr in basket.prepared:
            if pr.modification is not None:
                await self.check_modification(mode_product_be_add=pr.modification, product_id=pr.product_id)
            product_basket_create = ProductBasketTable(
                basket_id=basket_create.id, product_id=pr.product_id,
                count=pr.count,
            )
            self.session.add(product_basket_create)
            try:
                await self.session.flush()
            except IntegrityError:
                await self.session.rollback()
            if pr.modification is not None:
                product_modification_create = ProductBasketModificationTable(
                    product_basket_id=product_basket_create.id, modification=pr.modification)
                self.session.add(product_modification_create)

    async def update_product_basket(self, product_basket: list[ProductBasket], user_id: UserId):
        stmt = select(BasketTable).where(
            BasketTable.user_id == user_id, BasketTable.status == BasketStatus.prepare,
        )
        basket = (await self.session.execute(stmt)).scalars().first()
        stmt_delete = delete(ProductBasketTable).where(ProductBasketTable.basket_id == basket.id)
        await self.session.execute(stmt_delete)
        for pr in product_basket:
            if pr.modification is not None:
                await self.check_modification(mode_product_be_add=pr.modification, product_id=pr.product_id)
            product_basket_create = ProductBasketTable(
                basket_id=basket.id, product_id=pr.product_id,
                count=pr.count,
            )
            self.session.add(product_basket_create)
            try:
                await self.session.flush()
            except IntegrityError:
                await self.session.rollback()
                raise ProductNotFound(product_id=product_basket_create.product_id)
            if pr.modification is not None:
                product_modification_create = ProductBasketModificationTable(
                    product_basket_id=product_basket_create.id, modification=pr.modification)
                self.session.add(product_modification_create)

    async def check_modification(self, mode_product_be_add: int, product_id: int) -> None:
        stmt = select(ProductPriceTable.id).where(ProductPriceTable.product_id == product_id)
        result = (await self.session.execute(stmt)).scalars().all()
        for i in result:
            if i == mode_product_be_add:
                return
        raise ModificationSelectedError

    async def read_current_basket(self, user_id: UserId, language: Language) -> BasketViewInput | None:
        stmt = select(
            BasketTable.user_id, ProductTable.id, ProductImageTable.image,
            ProductNameTable.name, ProductBasketModificationTable.modification, ProductPriceNameTable.name,
            ProductBasketTable.count, ProductPriceTable.price,
        ).select_from(BasketTable).join(
            ProductBasketTable, BasketTable.id == ProductBasketTable.basket_id
        ).join(
            ProductTable, ProductBasketTable.product_id == ProductTable.id
        ).join(
            ProductNameTable, ProductTable.id == ProductNameTable.product_id
        ).outerjoin(
            ProductImageTable, ProductTable.id == ProductImageTable.product_id
        ).join(
            ProductPriceTable, ProductTable.id == ProductPriceTable.product_id
        ).outerjoin(
            ProductPriceNameTable, ProductPriceNameTable.price_id == ProductPriceTable.id
        ).outerjoin(
            ProductBasketModificationTable, ProductBasketTable.id == ProductBasketModificationTable.product_basket_id
        ).where(
            ProductNameTable.language == language, BasketTable.user_id == user_id,
            BasketTable.status == BasketStatus.prepare,
            case(
                (ProductPriceNameTable.language.is_not(None), ProductPriceNameTable.language == language),
                else_=True,
            ),
            case(
                (
                    ProductBasketModificationTable.modification.is_not(None),
                    ProductBasketModificationTable.modification == ProductPriceTable.id
                ),
                else_=True,
            )
        ).order_by(ProductTable.id, ProductPriceTable.id)
        result = (await self.session.execute(stmt)).all()
        if len(result) == 0:
            return None
        return serialize_basket_view(payload=result)

    async def read_restaurant_location(self, location_id: LocationId) -> Location:
        stmt = select(RestaurantLocationsTable.longitude, RestaurantLocationsTable.latitude).where(
            RestaurantLocationsTable.id == location_id
        )
        result = (await self.session.execute(stmt)).first()
        if result is None:
            return None
        return Location(longitude=result[0], latitude=result[1])

    async def get_banners(self, restaurant_id: RestaurantId) -> list[str]:
        stmt = select(RestaurantBannerTable.banner_url).where(
            RestaurantBannerTable.restaurant_id == restaurant_id
        ).order_by(RestaurantBannerTable.id)
        result = (await self.session.execute(stmt)).all()
        return [i[0] for i in result]

    async def get_addresses(self, restaurant_id: RestaurantId) -> list[tuple]:
        stmt = select(RestaurantLocationsTable.id, RestaurantLocationsTable.address).where(
            RestaurantLocationsTable.restaurant_id == restaurant_id
        )
        result = (await self.session.execute(stmt)).all()
        return result

    async def read_restaurant_data(self, restaurant_id: RestaurantId, language: Language) -> RestaurantView:
        stmt = select(
            RestaurantTable.id, RestaurantNameDescriptionTable.name,
            RestaurantNameDescriptionTable.description,
            RestaurantLocationsTable.id, RestaurantLocationsTable.address,
            RestaurantLocationsTable.latitude, RestaurantLocationsTable.longitude,
        ).select_from(RestaurantTable).join(
            RestaurantNameDescriptionTable, RestaurantTable.id == RestaurantNameDescriptionTable.restaurant_id
        ).join(
            RestaurantLocationsTable, RestaurantTable.id == RestaurantLocationsTable.restaurant_id
        ).where(RestaurantTable.id == restaurant_id, RestaurantNameDescriptionTable.language == language)
        result = (await self.session.execute(stmt)).all()
        if len(result) == 0:
            return None
        return serialize_restaurant_info(payload=result)

    async def get_restaurant(self, token: str) -> int | None:
        stmt = select(RestaurantTable.id).where(RestaurantTable.token == token)
        result = (await self.session.execute(stmt)).scalars().first()
        return result

    async def read_restaurant_location(self, location_id: LocationId) -> RestaurantLocation | None:
        stmt = select(RestaurantLocationsTable).where(RestaurantLocationsTable.id == location_id)
        result: RestaurantLocationsTable = (await self.session.execute(stmt)).scalars().first()
        if result is None:
            return None
        return RestaurantLocation(
            id=result.id, address=result.address,
            longitude=result.longitude, latitude=result.latitude,
        )

    async def read_categories(self, restaurant_id: RestaurantId, language: Language) -> list[Category]:
        stmt = select(CategoriesTable.id, CategoryNameTable.category).join(
            CategoryNameTable, CategoriesTable.id == CategoryNameTable.category_id
        ).where(CategoriesTable.restaurant_id == restaurant_id, CategoryNameTable.language == language)
        result = (await self.session.execute(stmt)).all()
        return serialize_category(payload=result)

    async def read_category_products(
            self, location_id: LocationId, language: Language, category_id: CategoryId,
    ) -> list[AdminProductsView] | None:
        stmt = select(
            CategoryNameTable.category, MenuProductTable.id, ProductNameTable.name, MenuProductTable.status,
        ).select_from(MenuProductTable).join(
            ProductNameTable, MenuProductTable.product_id == ProductNameTable.product_id
        ).join(
            CategoryNameTable, MenuProductTable.category_id == CategoryNameTable.category_id
        ).join(
            ProductTable, MenuProductTable.product_id == ProductTable.id
        ).where(
            MenuProductTable.location_id == location_id, ProductNameTable.language == language,
            CategoryNameTable.category_id == category_id, CategoryNameTable.language == language,
            MenuProductTable.status == MenuProductStatus.available, ProductTable.status == ProductStatus.active,
        ).order_by(ProductTable.id)
        result = (await self.session.execute(stmt)).all()
        if len(result) == 0:
            return None
        return serialize_admin_category_products(payload=result)

    async def read_restaurant_locations_id(self, restaurant_id: RestaurantId) -> list[LocationId]:
        stmt = select(RestaurantLocationsTable.id).where(RestaurantLocationsTable.restaurant_id == restaurant_id)
        result = (await self.session.execute(stmt)).scalars().all()
        return result

    async def create_product(self, product: Product) -> ProductId:
        main_table = ProductTable(mode=product.mode, status=product.status)
        self.session.add(main_table)
        await self.session.flush()
        if product.photo is not None:
            product_image = ProductImageTable(product_id=main_table.id, image=product.photo)
            self.session.add(product_image)
        for name in product.name:
            self.session.add(ProductNameTable(
                product_id=main_table.id, name=name.name, language=name.language,
            ))
        if product.description is not None:
            for desc in product.description:
                self.session.add(ProductDescriptionTable(
                    product_id=main_table.id, description=desc.description, language=desc.language,
                ))
        for price in product.price:
            if len(price.name) == 0:
                self.session.add(ProductPriceTable(
                    product_id=main_table.id, price=price.price,
                ))
                break
            else:
                pr = ProductPriceTable(product_id=main_table.id, price=price.price)
                self.session.add(pr)
                await self.session.flush()
                for price_name in price.name:
                    self.session.add(ProductPriceNameTable(
                        price_id=pr.id, name=price_name.name, language=price_name.language,
                    ))
        return main_table.id

    async def create_menu_product(
            self, locations_id: list[LocationId], category_id: CategoryId,
            product_id: ProductId,
    ) -> None:
        for loc_id in locations_id:
            self.session.add(MenuProductTable(
                location_id=loc_id, category_id=category_id, product_id=product_id,
                status=MenuProductStatus.available,
            ))

    async def read_branches(self, restaurant_id: RestaurantId) -> list[ReadRestaurantBranches] | None:
        stmt = select(RestaurantLocationsTable.id, RestaurantLocationsTable.address).where(
            RestaurantLocationsTable.restaurant_id == restaurant_id
        )
        result = (await self.session.execute(stmt)).all()
        if len(result) == 0:
            return None
        return [ReadRestaurantBranches(location_id=br[0], address=br[1]) for br in result]

    async def get_product_by_menu_product_id(self, menu_product_id: ProductId) -> ProductAdmin | None:
        stmt = select(
            MenuProductTable.product_id, ProductImageTable.image, ProductNameTable.name, ProductNameTable.language,
            ProductDescriptionTable.description, ProductDescriptionTable.language, ProductTable.mode,
            ProductPriceTable.id, ProductPriceTable.price, ProductPriceNameTable.name, ProductPriceNameTable.language,
            ProductTable.status, MenuProductTable.status,
        ).select_from(MenuProductTable).join(
            ProductTable, MenuProductTable.product_id == ProductTable.id
        ).outerjoin(
            ProductImageTable, ProductTable.id == ProductImageTable.product_id
        ).join(
            ProductNameTable, ProductTable.id == ProductNameTable.product_id
        ).outerjoin(
            ProductDescriptionTable, ProductTable.id == ProductDescriptionTable.product_id
        ).join(
            ProductPriceTable, ProductTable.id == ProductPriceTable.product_id
        ).outerjoin(
            ProductPriceNameTable, ProductPriceTable.id == ProductPriceNameTable.price_id
        ).where(MenuProductTable.id == menu_product_id)
        result = (await self.session.execute(stmt)).all()
        if len(result) == 0:
            return None
        return show_product_admin(payload=result)

    async def get_product_location(self, menu_product_id: int) -> MenuProduct | None:
        stmt = select(
            MenuProductTable.location_id, MenuProductTable.category_id,
            MenuProductTable.product_id, MenuProductTable.status,
        ).where(MenuProductTable.id == menu_product_id)
        result = (await self.session.execute(stmt)).first()
        if result is None:
            return None
        return MenuProduct(
            location_id=result[0], category_id=result[1],
            product_id=result[2], status=result[3],
        )

    async def edit_product_available(self, menu_product_id: int, status: MenuProductStatus) -> None:
        stmt = update(MenuProductTable).where(
            MenuProductTable.id == menu_product_id
        ).values({MenuProductTable.status: status})
        await self.session.execute(stmt)

    async def get_product_by_product_id(self, product_id: ProductId) -> Product | None:
        stmt = select(
            ProductTable.id, ProductImageTable.image, ProductNameTable.name, ProductNameTable.language,
            ProductDescriptionTable.description, ProductDescriptionTable.language, ProductTable.mode,
            ProductPriceTable.id, ProductPriceTable.price, ProductPriceNameTable.name, ProductPriceNameTable.language,
            ProductTable.status,
        ).select_from(ProductTable).outerjoin(
            ProductImageTable, ProductTable.id == ProductImageTable.product_id
        ).join(
            ProductNameTable, ProductTable.id == ProductNameTable.product_id
        ).outerjoin(
            ProductDescriptionTable, ProductTable.id == ProductDescriptionTable.product_id
        ).join(
            ProductPriceTable, ProductTable.id == ProductPriceTable.product_id
        ).outerjoin(
            ProductPriceNameTable, ProductPriceTable.id == ProductPriceNameTable.price_id
        ).where(ProductTable.id == product_id)
        result = (await self.session.execute(stmt)).all()
        if len(result) == 0:
            return None
        return show_product_core(payload=result)

    async def edit_product_photo(self, photo: str, product_id: ProductId) -> None:
        stmt = update(ProductImageTable).where(
            ProductImageTable.product_id == product_id
        ).values({ProductImageTable.image: photo})
        await self.session.execute(stmt)

    async def add_product_photo(self, photo: str, product_id: ProductId) -> None:
        product_photo = ProductImageTable(product_id=product_id, image=photo)
        self.session.add(product_photo)

    async def edit_product_name(self, name: list[ProductName], product_id: ProductId) -> None:
        stmt = delete(ProductNameTable).where(ProductNameTable.product_id == product_id)
        await self.session.execute(stmt)
        for n in name:
            product_name = ProductNameTable(product_id=product_id, name=n.name, language=n.language)
            self.session.add(instance=product_name)

    async def edit_product_description(self, description: list[ProductDescription], product_id: ProductId) -> None:
        stmt = delete(ProductDescriptionTable).where(ProductDescriptionTable.product_id == product_id)
        await self.session.execute(stmt)
        for n in description:
            product_description = ProductDescriptionTable(
                product_id=product_id, description=n.description, language=n.language,
            )
            self.session.add(instance=product_description)

    async def add_product_description(self, description: list[ProductDescription], product_id: ProductId) -> None:
        for n in description:
            product_description = ProductDescriptionTable(
                product_id=product_id, description=n.description, language=n.language,
            )
            self.session.add(instance=product_description)

    async def edit_product_price(self, price: list[ProductPrice], product_id: ProductId) -> None:
        stmt = delete(ProductPriceTable).where(ProductPriceTable.product_id == product_id)
        await self.session.execute(stmt)
        for p in price:
            product_price = ProductPriceTable(
                product_id=product_id, price=p.price,
            )
            self.session.add(instance=product_price)
            await self.session.flush()
            for n in p.name:
                product_price_name = ProductPriceNameTable(
                    price_id=product_price.id, name=n.name, language=n.language)
                self.session.add(product_price_name)

    async def read_stop_list(self, location_id: LocationId, language: Language) -> list[StopList] | None:
        stmt = select(MenuProductTable.id, ProductNameTable.name).select_from(
            MenuProductTable
        ).join(
            ProductNameTable, MenuProductTable.product_id == ProductNameTable.product_id
        ).where(
            MenuProductTable.location_id == location_id, ProductNameTable.language == language,
            MenuProductTable.status == MenuProductStatus.not_available,
        )
        result = (await self.session.execute(stmt)).all()
        if len(result) == 0:
            return None
        return [
            StopList(menu_product_id=stop[0], name=stop[1]) for stop in result
        ]

    async def delete_product(self, product_id: ProductId) -> None:
        stmt = update(ProductTable).where(
            ProductTable.id == product_id).values(
            {ProductTable.status: ProductStatus.deleted},
        )
        await self.session.execute(stmt)

    async def read_restaurant_addresses(self, restaurant_id: RestaurantId) -> list[str] | None:
        stmt = select(RestaurantLocationsTable.address).where(
            RestaurantLocationsTable.restaurant_id == restaurant_id).order_by(RestaurantLocationsTable.id)
        result = (await self.session.execute(stmt)).scalars().all()
        if len(result) == 0:
            return None
        return [address for address in result]

    async def read_user_addresses(self, user_id: UserId) -> list[str]:
        stmt = select(ShippingOrderTable.address, ShippingOrderTable.id).select_from(
            ShippingOrderTable
        ).join(
            OrderTable, ShippingOrderTable.order_id == OrderTable.id
        ).join(
            UserAddressTable, UserAddressTable.order_id == OrderTable.id
        ).where(OrderTable.user_id == user_id).order_by(
            desc(ShippingOrderTable.id)
        ).limit(3)
        result = (await self.session.execute(stmt)).all()
        return [address[0] for address in result]

    async def read_restaurant_location_id_by_address(self, restaurant_id: RestaurantId, address: str) -> int:
        stmt = select(RestaurantLocationsTable.id).where(
            RestaurantLocationsTable.restaurant_id == restaurant_id,
            RestaurantLocationsTable.address == address,
        )
        result = (await self.session.execute(stmt)).scalars().first()
        return result

    async def read_user_location_by_address(self, address: str, user_id: UserId) -> Location | None:
        stmt = select(ShippingLocationTable.longitude, ShippingLocationTable.latitude).join(
            ShippingOrderTable, ShippingOrderTable.id == ShippingLocationTable.shipping_id
        ).join(
            OrderTable, ShippingOrderTable.order_id == OrderTable.id
        ).where(ShippingOrderTable.address == address, OrderTable.user_id == user_id)
        result = (await self.session.execute(stmt)).first()
        if result is None:
            return None
        return Location(longitude=result[0], latitude=result[1])

    async def create_pick_up_order(self, order: PickUpOrder) -> OrderId:
        create_order = OrderTable(
            user_id=order.user_id, phone=order.phone, order_type=order.order_type,
            amount=order.amount, payment_type=order.payment_type, status=order.status,
        )
        self.session.add(create_order)
        await self.session.flush()
        await self.add_products_to_order(order_id=create_order.id, products=order.products)
        return create_order.id

    async def create_shipping_order(self, order: ShippingOrder) -> OrderId:
        create_order = OrderTable(
            user_id=order.user_id, phone=order.phone, order_type=order.order_type,
            amount=order.amount, payment_type=order.payment_type, status=order.status,
        )
        self.session.add(create_order)
        await self.session.flush()
        await self.add_products_to_order(order_id=create_order.id, products=order.products)
        shipping_part = ShippingOrderTable(
            order_id=create_order.id, address=order.address, comment=order.comment,
            shipping_length=order.shipping_length, total_amount=order.total_amount,
        )
        self.session.add(shipping_part)
        await self.session.flush()
        shipping_location = ShippingLocationTable(
            shipping_id=shipping_part.id, latitude=order.location.latitude,
            longitude=order.location.longitude,
        )
        self.session.add(shipping_location)
        return create_order.id

    async def exist_user_address(self, address: str, user_id: UserId) -> bool:
        stmt = select(ShippingOrderTable.address).select_from(ShippingOrderTable).join(
            OrderTable, ShippingOrderTable.order_id == OrderTable.id
        ).where(OrderTable.user_id == user_id, ShippingOrderTable.address == address)
        result = (await self.session.execute(stmt)).scalars().first()
        return bool(result)

    async def add_address_to_pool(self, order_id: OrderId) -> None:
        address = UserAddressTable(order_id=order_id)
        self.session.add(address)

    async def add_products_to_order(self, order_id: OrderId, products: list[ProductOrder]):
        for product in products:
            add_product = ProductOrderTable(
                order_id=order_id, product_id=product.product_id,
                modification=0 if product.modification is None else product.modification,
                count=product.count, price=product.price,
            )
            self.session.add(add_product)

    async def accept_order(self, order_id: OrderId) -> UserId:
        stmt = update(
            OrderTable
        ).where(OrderTable.id == order_id).values({OrderTable.status: OrderStatus.accepted}).returning(
            OrderTable.user_id)
        result = (await self.session.execute(stmt)).scalars().first()
        return result

    async def telegram_id_from_user_id(self, user_id: UserId) -> tuple:
        stmt = select(TelegramUserTable.telegram_id, UserTable.language).join(
            UserTable, TelegramUserTable.user_id == UserTable.id
        ).where(TelegramUserTable.user_id == user_id)
        result = (await self.session.execute(stmt)).first()
        return result

    async def exist_order(self, order_id: OrderId) -> bool:
        stmt = select(OrderTable.id).where(OrderTable.id == order_id)
        result = (await self.session.execute(stmt)).scalars().first()
        if result is None:
            return False
        return True

    async def read_branch_group(self, restaurant_location_id: int) -> int:
        stmt = select(GroupTable.group_id).where(GroupTable.restaurant_location_id == restaurant_location_id)
        group_id = (await self.session.execute(stmt)).scalars().first()
        return group_id

    async def read_order_admin(self, order_id: OrderId) -> ReadOrderAdmin | None:
        stmt = select(
            OrderTable.id, UserTable.name, OrderTable.phone, OrderTable.payment_type, ShippingOrderTable.address,
            ShippingOrderTable.comment, ShippingLocationTable.longitude, ShippingLocationTable.latitude,
            OrderTable.amount, ShippingOrderTable.total_amount,
        ).select_from(
            OrderTable
        ).join(
            UserTable, OrderTable.user_id == UserTable.id
        ).outerjoin(
            ShippingOrderTable, OrderTable.id == ShippingOrderTable.order_id
        ).outerjoin(
            ShippingLocationTable, ShippingOrderTable.id == ShippingLocationTable.shipping_id
        ).join(
            ProductOrderTable, OrderTable.id == ProductOrderTable.order_id,
        ).where(OrderTable.id == order_id)
        result = (await self.session.execute(stmt)).first()
        if result is None:
            return None
        return serialize_admin_order(payload=result)

    async def read_admin_order_product(self, order_id: OrderId, language: Language) -> list[ReadAdminOrderProduct]:
        stmt = select(ProductNameTable.name, ProductPriceNameTable.name, ProductOrderTable.count).select_from(
            ProductOrderTable
        ).join(
            ProductNameTable, ProductOrderTable.product_id == ProductNameTable.product_id
        ).outerjoin(
            ProductPriceNameTable, ProductOrderTable.modification == ProductPriceNameTable.price_id
        ).where(
            ProductNameTable.language == language,
            case(
                (ProductPriceNameTable.language.is_not(None), ProductPriceNameTable.language == language),
                else_=True,
            ),
            ProductOrderTable.order_id == order_id,
        )
        result = (await self.session.execute(stmt)).all()
        return serialize_admin_product(payload=result)

    async def read_order_user(self, order_id: OrderId) -> ReadOrderUser | None:
        stmt = select(
            OrderTable.id, OrderTable.amount, ShippingOrderTable.total_amount,
        ).select_from(OrderTable).outerjoin(
            ShippingOrderTable, OrderTable.id == ShippingOrderTable.order_id
        ).where(OrderTable.id == order_id)
        result = (await self.session.execute(stmt)).first()
        if result is None:
            return None
        return serialize_user_order(payload=result)

    async def read_user_order_product(self, order_id: OrderId, language: Language) -> list[ReadUserOrderProduct]:
        stmt = select(
            ProductNameTable.name, ProductPriceNameTable.name,
            ProductPriceTable.price, ProductOrderTable.count,
        ).select_from(ProductOrderTable).join(
            ProductNameTable, ProductOrderTable.product_id == ProductNameTable.product_id
        ).join(
            ProductPriceTable,
            case(
                (ProductOrderTable.modification != 0, ProductOrderTable.modification == ProductPriceTable.id),
                else_=ProductOrderTable.product_id == ProductPriceTable.product_id,
            ),
        ).outerjoin(
            ProductPriceNameTable, ProductOrderTable.modification == ProductPriceNameTable.price_id
        ).where(
            ProductNameTable.language == language,
            case(
                (ProductPriceNameTable.language.is_not(None), ProductPriceNameTable.language == language),
                else_=True,
            ),
            ProductOrderTable.order_id == order_id,
        )
        result = (await self.session.execute(stmt)).all()
        return serialize_user_product(payload=result)
