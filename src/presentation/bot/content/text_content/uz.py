from typing import Optional

from src.application.read_current_basket.dto import PreparedBasketProduct
from src.domain.order.entities.order import OrderId, Location
from src.domain.order.entities.order_view import ReadUserOrderProduct, ReadAdminOrderProduct
from src.domain.user.constants.user import Language
from src.presentation.bot.content.content_enums import ExistingTypes
from src.presentation.bot.content.format.format_manager import FormatManager
from src.presentation.bot.content.text_content.constants import ConcretePaymentType
from src.presentation.bot.content.text_content.interfaces import IText


class UzbekText(IText):
    language = Language.uz

    def __init__(self, format: FormatManager):
        self.format = format

    def user_promoted_to_admin(self, mention: str) -> str:
        return f"Новый администратор! {mention}"

    def admin_restricted_to_user(self, mention: str) -> str:
        return f"Участник исключен из администраторов! {mention}"

    def administrators_updated(self) -> str:
        return "Администраторы обновлены!"

    def greeting(self) -> str:
        return (
            "Telegrambotga sushi master hush kelibsiz!\n\n"
            "Nimadur tanlaymizmi? 😋"
        )

    def restaurant_info(self, name: str, description: str) -> str:
        return f"{name}\n{description}"

    def location_address(self, address: str) -> str:
        return f"📍Filiali: <b>{address}</b>"

    def profile_settings_text(self, name: str, phone: Optional[str], language: Language) -> str:
        return (f"<b>Ismi</b>: {name}\n<b>Telefon:</b> {phone if phone else 'Yozish qutilmoqta...'}\n"
                f"<b>Til:</b> 🇺🇿 {language}")

    def input_name(self) -> str:
        return "Ismingizni kiriting 👇"

    def input_phone(self) -> str:
        return (
            "Telefon nomer kiriting 👇\n\n«📱 Meni nomerim» knopkani bosish mumkun yoki\n"
            "qoli bilan kirgizish mumkun: +998901234567"
        )

    def input_language(self) -> str:
        return "Tilini tanlan 👇"

    def choose_order_method(self) -> str:
        return "Выберите тип заказа 👇"

    def send_location_in_pickup(self) -> str:
        return "Выберите филиал либо отправьте локацию и мы определим ближайший к вам 👇"

    def send_location_in_shipping(self) -> str:
        return (
            "📍 Отправьте локацию либо выберите адрес доставки 👇\n\n"
            "<i>Доставка за пределы города не осуществляется. Время доставки от 40 минут</i>"
        )

    def show_webapp_button_in_pick_up(self, address: str) -> str:
        return f"Филиал <b>{address}</b>"

    def show_webapp_button_in_shipping(self, address: str) -> str:
        return f"<b>Ваш адрес</b>\n\n{address}"

    def restaurant_address_not_found(self) -> str:
        return "Адрес ресторана не найден ⛔️"

    def user_address_not_found(self) -> str:
        return "Выберите адрес из списка ниже, если они там есть ⛔️"

    def get_comment(self) -> str:
        return (
            "Введите дополнительную информацию по адресу.\n"
            "<b>Например:</b> № подъезда, этаж, код от двери, № квартиры и тд..."
        )

    def get_phone(self) -> str:
        return (
            "Отправьте или введите ваш номер телефона\nв формате: +998** *** ** **\n\n"
            "Примечание: Если вы планируете оплатить заказ онлайн с помощью Click либо Payme,"
            "пожалуйста, укажите номер телефона, на который зарегистрирован "
            "аккаунт в соответствующем сервисе"
        )

    def accept_order_pickup(
            self, phone: str, products: list[PreparedBasketProduct], total_amount: int,
    ) -> str:
        return (
            f"<b>Ваш заказ:</b>\n\n<b>Тип заказа:</b> 🚶 Самовывоз\n"
            f"<b>Телефон:</b> {phone}\n"
            f"{self.format(ExistingTypes.Text).format_products_view(products=products, currency_name='сум')}"
            f"\n\n<b>Итого  — {self.format(ExistingTypes.Text).format_product_price(total_amount)} "
            f"сум</b>\n\nВсе верно?"
        )

    def accept_order_shipping(
            self, comment: str, phone: str, address: str, shipping_length: float,
            products: list[PreparedBasketProduct], amount: int, shipping_amount: int,
            total_amount: int,
    ) -> str:
        return (
            f"<b>Ваш заказ:</b>\n\n<b>"
            f"Тип заказа:</b> 🛵 Доставка\n"
            f"<b>Телефон:</b> {phone}\n"
            f"<b>Адрес:</b> {address}\n"
            f"<b>Комментарий:</b> {comment}\n"
            f"{self.format(ExistingTypes.Text).format_products_view(products=products, currency_name='сум')}"
            f"\n\n<b>Сумма заказа: {self.format(ExistingTypes.Text).format_product_price(amount)} сум</b>"
            f"\n\nСтоимость доставки — {self.format(ExistingTypes.Text).format_product_price(shipping_amount)} сум"
            f"\n<i>Ориентировочное расстояние от филиала: {shipping_length} км</i>"
            f"\n\n<b>Итого  — {self.format(ExistingTypes.Text).format_product_price(total_amount)} сум</b>"
            f"\n\nВсе верно?"
        )

    def choose_type_charge(self) -> str:
        return "Выберите способ оплаты 👇"

    def send_url_for_charge_payme(self, total_amount: str, order_id: OrderId) -> str:
        return (
            f"Оплата <b>Payme</b> на сумму <b>{total_amount}</b> сум.\n"
            f"Номер заказа <b>#{order_id}</b>\n"
            f"Для оплаты нажмите на кнопку 👇"
        )

    def send_url_for_charge_click(self, total_amount: str, order_id: OrderId) -> str:
        return (
            f"Оплата <b>Click</b> на сумму <b>{total_amount}</b> сум.\n"
            f"Номер заказа <b>#{order_id}</b>\n"
            f"Для оплаты нажмите на кнопку 👇"
        )

    def successfully_payment(self) -> str:
        return "✅ Оплата прошла успешно"

    def send_finish_order_presentation_pickup(
            self, order_id: OrderId, products: list[ReadUserOrderProduct],
            total_amount: int,
    ) -> str:
        return (
            f"Ваш заказ принят, ориентировочное время готовности 20 минут. Номер вашего заказа #{order_id}.\n"
            f"{self.format(ExistingTypes.Text).format_products_view_user(products=products, currency_name='сум')}"
            f"\n\n<b>Итого  — {total_amount} сум</b>\n\nХорошего дня!"
        )

    def send_finish_order_presentation_shipping(
            self, order_id: OrderId, products: list[ReadUserOrderProduct],
            shipping_amount: int, total_amount: int,
    ) -> str:
        return (
            f"Ваш заказ принят, ориентировочное время готовности 20 минут. Номер вашего заказа #{order_id}.\n"
            f"{self.format(ExistingTypes.Text).format_products_view_user(products=products, currency_name='сум')}"
            f"\n\nСтоимость доставки — {self.format(ExistingTypes.Text).format_product_price(shipping_amount)} сум"
            f"\n<b>Итого  — {self.format(ExistingTypes.Text).format_product_price(total_amount)} сум</b>"
            f"\n\nХорошего дня!"
        )

    def send_order_to_admins_pickup(
            self, order_id: OrderId, products: list[ReadAdminOrderProduct],
            first_name: str, phone: str, payment_type: ConcretePaymentType, total_amount: int,
    ):
        return (
            f"<b>Заказ #{order_id}</b> — 🚶 Самовывоз\n"
            f"{self.format(ExistingTypes.Text).format_products_view_admin(products=products)}\n\n"
            f"<b>Ф.И.О:</b> {first_name}\n"
            f"<b>Телефон:</b> {phone}\n"
            f"<b>Способ оплаты:</b> {payment_type}\n\n"
            f"<b>Сумма заказа:</b> {self.format(ExistingTypes.Text).format_product_price(total_amount)} сум"
        )

    def send_order_to_admins_shipping(
            self, order_id: OrderId, products: list[ReadAdminOrderProduct],
            first_name: str, phone: str, payment_type: ConcretePaymentType, address: str, comment: str,
            shipping_amount: int, total_amount: int, user_location: Location,
    ):
        return (
            f"<b>Заказ #{order_id}</b> — 🚶 Самовывоз\n"
            f"{self.format(ExistingTypes.Text).format_products_view_admin(products=products)}\n\n"
            f"<b>Ф.И.О:</b> {first_name}\n"
            f"<b>Телефон:</b> {phone}\n"
            f"<b>Способ оплаты:</b> {payment_type}\n"
            f"<b>Адрес:</b> {address}\n"
            f"<b>Комментарий:</b> {comment}\n\n"
            f"<b>Сумма заказа:</b> {self.format(ExistingTypes.Text).format_product_price(total_amount)} сум\n\n"
            f"<b>Доставка:</b> {self.format(ExistingTypes.Text).format_product_price(shipping_amount)} сум"
        )

    def accept_order_pickup_by_admin(self, order_id: OrderId) -> str:
        return (f"Заказ #{order_id} в процессе приготовления. "
                f"Ориентировочное время готовности 20 минут.")

    def accept_order_shipping_by_admin(self, order_id: OrderId) -> str:
        return (f"Ваш заказ принят и будет отправлен в указанный срок. "
                f"Номер вашего заказа #{order_id}.")

    def wrong_phone_number(self) -> str:
        return ("⛔️ Неверно введен номер телефона, попробуйте снова. "
                "Отправьте или введите ваш номер телефона\nв формате: +998** *** ** **")

    def wrong_comment_length(self) -> str:
        return "⛔️ Слишком длинный комментарий, пожалуйста опишите то что вы хотите более кратко"

    def no_comment(self) -> str:
        return "Комментариев нет"

    def select_branches_attach_group(self) -> str:
        return "Выберите филиалы к которым хотите присоеденить текущую группу"

    def empty_basket_error(self) -> str:
        return "В корзине ничего нет ⛔️"

    def critical_error(self) -> str:
        return "Что то пошло не так..."
