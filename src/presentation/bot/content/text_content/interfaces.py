from typing import Protocol, Optional

from src.application.read_current_basket.dto import PreparedBasketProduct
from src.domain.order.entities.order import OrderId, Location
from src.domain.order.entities.order_view import ReadUserOrderProduct
from src.domain.product.constants.product import ProductMode
from src.domain.product.entities.product import ProductName, ProductDescription
from src.domain.product.entities.product_view import AdminProductPrice
from src.domain.restaurant.constants.constants import MenuProductStatus
from src.domain.user.constants.user import Language
from src.presentation.bot.content.content_enums import ExistingTypes
from src.presentation.bot.content.text_content.constants import ConcretePaymentType
from src.presentation.bot.states.state_data.product import ProductNameData, ProductDescriptionData, ProductPriceData


class IText(Protocol):
    language: Language

    def greeting(self) -> str:
        raise NotImplementedError

    def restaurant_info(self, name: str, description: str) -> str:
        raise NotImplementedError

    def location_address(self, address: str) -> str:
        raise NotImplementedError

    def leave_feedback(self) -> str:
        raise NotImplementedError

    def promise_delivery_feedback(self) -> str:
        raise NotImplementedError

    def profile_settings_text(self, name: str, phone: Optional[str], language: Language) -> str:
        raise NotImplementedError

    def input_name(self) -> str:
        raise NotImplementedError

    def input_phone(self) -> str:
        raise NotImplementedError

    def input_language(self) -> str:
        raise NotImplementedError

    def greeting_administrator(self) -> str:
        raise NotImplementedError

    def choose_something(self) -> str:
        raise NotImplementedError

    def categories(self) -> str:
        raise NotImplementedError

    def uploading_product(
            self, photo: str, name: list[ProductNameData],
            description: Optional[list[ProductDescriptionData]],
            price: list[ProductPriceData],
    ) -> str:
        raise NotImplementedError

    def upload_photo_text(self) -> str:
        raise NotImplementedError

    def upload_name_text(self, language: Language) -> str:
        raise NotImplementedError

    def upload_description_text(self, language: Language) -> str:
        raise NotImplementedError

    def upload_price_text(self) -> str:
        raise NotImplementedError

    def upload_price_name_text(self, language: Language) -> str:
        raise NotImplementedError

    def choose_mode(self) -> str:
        raise NotImplementedError

    def finish_create_product(self) -> str:
        raise NotImplementedError

    def category_not_found_in_add_product(self) -> str:
        raise NotImplementedError

    def name_not_found_in_add_product(self) -> str:
        raise NotImplementedError

    def description_not_full(self) -> str:
        raise NotImplementedError

    def price_is_empty(self) -> str:
        raise NotImplementedError

    def price_name_not_found_in_add_product(self) -> str:
        raise NotImplementedError

    def choose_branch(self) -> str:
        raise NotImplementedError

    def location_id_not_found(self) -> str:
        raise NotImplementedError

    def something_went_wrong(self) -> str:
        raise NotImplementedError

    def category_products_empty(self) -> str:
        raise NotImplementedError

    def admin_product(
            self, name: list[ProductName], description: Optional[list[ProductDescription]],
            mode: ProductMode, price: list[AdminProductPrice], menu_product_status: MenuProductStatus,
    ) -> str:
        raise NotImplementedError

    def price_must_be_integer(self) -> str:
        raise NotImplementedError

    def list_is_empty(self) -> str:
        raise NotImplementedError

    def change_menu_product_status_call_answer(self, status: MenuProductStatus) -> str:
        raise NotImplementedError

    def access_delete_product(self) -> str:
        raise NotImplementedError

    def choose_order_method(self) -> str:
        raise NotImplementedError

    def send_location_in_pickup(self) -> str:
        raise NotImplementedError

    def send_location_in_shipping(self) -> str:
        raise NotImplementedError

    def show_webapp_button_in_pick_up(self, address: str) -> str:
        raise NotImplementedError

    def show_webapp_button_in_shipping(self, address: str) -> str:
        raise NotImplementedError

    def restaurant_address_not_found(self) -> str:
        raise NotImplementedError

    def user_address_not_found(self) -> str:
        raise NotImplementedError

    def get_comment(self) -> str:
        raise NotImplementedError

    def get_phone(self) -> str:
        raise NotImplementedError

    def accept_order_pickup(
            self, phone: str, products: list[PreparedBasketProduct], total_amount: int,
    ) -> str:
        raise NotImplementedError

    def accept_order_shipping(
            self, comment: str, phone: str, address: str, shipping_length: float,
            products: list[PreparedBasketProduct], amount: int, shipping_amount: str,
            total_amount: int,
    ) -> str:
        raise NotImplementedError

    def choose_type_charge(self) -> str:
        raise NotImplementedError

    def send_url_for_charge_payme(self, total_amount: int, order_id: OrderId) -> str:
        raise NotImplementedError

    def send_url_for_charge_click(self, total_amount: str, order_id: OrderId) -> str:
        raise NotImplementedError

    def successfully_payment(self) -> str:
        raise NotImplementedError

    def send_finish_order_presentation_pickup(
            self, order_id: OrderId, products: list[ReadUserOrderProduct],
            total_amount: int,
    ) -> str:
        raise NotImplementedError

    def send_finish_order_presentation_shipping(
            self, order_id: OrderId, products: list[ReadUserOrderProduct],
            shipping_amount: int, total_amount: int,
    ) -> str:
        raise NotImplementedError

    def send_order_to_admins_pickup(
            self, order_id: OrderId, products: list[PreparedBasketProduct],
            first_name: str, phone: str, payment_type: ConcretePaymentType, total_amount: int,
    ):
        raise NotImplementedError

    def send_order_to_admins_shipping(
            self, order_id: OrderId, products: list[PreparedBasketProduct],
            first_name: str, phone: str, payment_type: ConcretePaymentType, address: str, comment: str,
            shipping_amount: int, total_amount: int, user_location: Location,
    ):
        raise NotImplementedError


class IFormat(Protocol):
    format: ExistingTypes
