from typing import Optional

from src.application.read_current_basket.dto import PreparedBasketProduct
from src.domain.order.constants.order import OrderType
from src.domain.order.entities.order import OrderId, Location
from src.domain.order.entities.order_view import ReadAdminOrderProduct, ReadUserOrderProduct
from src.domain.product.constants.product import ProductMode
from src.domain.product.entities.product import ProductName, ProductDescription
from src.domain.product.entities.product_view import AdminProductPrice
from src.domain.restaurant.constants.constants import MenuProductStatus
from src.domain.user.constants.user import Language
from src.presentation.bot.content.content_enums import ExistingTypes
from src.presentation.bot.content.format.format_manager import FormatManager
from src.presentation.bot.content.text_content.constants import ConcretePaymentTypeRu, ConcretePaymentType
from src.presentation.bot.content.text_content.interfaces import IText
from src.presentation.bot.states.state_data.product import (
    ProductNameData, ProductDescriptionData, ProductPriceData, ProductPriceNameData,
)


class RussianText(IText):
    language = Language.ru

    def __init__(self, format: FormatManager):
        self.format = format

    def user_promoted_to_admin(self, mention: str) -> str:
        return f"Новый администратор! {mention}"

    def admin_restricted_to_user(self, mention: str) -> str:
        return f"Участник исключен из администраторов! {mention}"

    def greeting(self) -> str:
        return (
            "Добро пожаловать в телеграм-бот SUSHI MASTER!\n\n"
            "Наберём чего-нибудь вкусненького? 😋"
        )

    def restaurant_info(self, name: str, description: str) -> str:
        return f"<b>{name}</b>\n{description}"

    def location_address(self, address: str) -> str:
        return f"📍Филиал: <b>{address}</b>"

    def profile_settings_text(self, name: str, phone: Optional[str], language: Language) -> str:
        return (f"<b>Ф.И.О</b>: {name}\n<b>Телефон:</b> {phone if phone else 'Ожидание записи...'}\n"
                f"<b>Язык:</b> 🇷🇺 {language}")

    def input_name(self) -> str:
        return "Введите Ф.И.О. 👇"

    def input_phone(self) -> str:
        return (
            "Отправьте номер телефона 👇\n\nМожно нажать «📱 Мой номер» или\n"
            "ввести вручную в формате: +998901234567"
        )

    def input_language(self) -> str:
        return "Выберите язык 👇"

    def greeting_administrator(self) -> str:
        return "Вы администратор!"

    def choose_something(self) -> str:
        return "Выберите одно из следующих"

    def categories(self) -> str:
        return "Выберите категорию 👇"

    def uploading_product(
            self, photo: str, name: list[ProductNameData],
            description: Optional[list[ProductDescriptionData]],
            price: list[ProductPriceData],
    ) -> str:
        product_name = self.format(ExistingTypes.Text).format_product_names(names=name)
        product_description = self.format(ExistingTypes.Text).format_product_descriptions(descriptions=description)
        product_price = self.format(ExistingTypes.Text).format_product_prices(prices=price)
        return (
            f"{'<b>Фото:</b> Ожидание записи ...' if photo is None else ''}\n"
            f"{'<b>Имя:</b> Ожидание записи ...' if len(name) == 0 else product_name}\n\n"
            f"{'<b>Описание:</b> Ожидание записи ...' if len(description) == 0 else product_description}\n\n"
            f"{'<b>Цена:</b> Ожидание записи ...' if len(price) == 0 else product_price}"
        )

    def upload_photo_text(self) -> str:
        return "Загрузите фото:"

    def upload_name_text(self, language: Language) -> str:
        return f"Введите имя на {language} языке:"

    def upload_description_text(self, language: Language) -> str:
        return f"Введите описание на {language} языке:"

    def upload_price_text(self) -> str:
        return "Введите цену:"

    def upload_price_name_text(self, language: Language) -> str:
        return f"Введите вид товара на {language} языке:"

    def choose_mode(self) -> str:
        return ("Выберите разновидность товара:\n\n"
                "В зависимости от количества разновидностей товара у "
                "него может быть либо <i>несколько цен</i> либо <i>одна цена</i>.\n"
                "<i><b>Обычный</b></i> тип это товар с одной ценой.\n"
                "<i><b>Расширенный</b></i> это товар с нескольких модификаций("
                "например, модификации могут различаться размером товара "
                "или добавками.)")

    def finish_create_product(self) -> str:
        return "Продукт создан! ✅"

    def category_not_found_in_add_product(self) -> str:
        return "Категория для продукта не заполнена!"

    def name_not_found_in_add_product(self) -> str:
        return "Название продукта не заполнено!"

    def description_not_full(self) -> str:
        return "В описании присутствуют не все языки, заполните до конца!"

    def price_is_empty(self) -> str:
        return "Цена товара пуста!"

    def price_name_not_found_in_add_product(self) -> str:
        return "В обозначении видов товаров, заполнены не все языки, заполните до конца!"

    def choose_branch(self) -> str:
        return "Выберите ресторан которым хотите управлять 👇"

    def location_id_not_found(self) -> str:
        return "Неизвестная ошибка, нажмите /admin и начните по новой"

    def something_went_wrong(self) -> str:
        return "Что-то пошло не так, пожалуйста нажмите /admin и начните по новой"

    def category_products_empty(self) -> str:
        return "Список пуст"

    def admin_product(
            self, name: list[ProductName], description: Optional[list[ProductDescription]],
            mode: ProductMode, price: list[AdminProductPrice], menu_product_status: MenuProductStatus,
    ) -> str:
        product_name = [ProductNameData(name=n.name, language=n.language) for n in name]
        product_description = [
            ProductDescriptionData(
                description=d.description,
                language=d.language,
            ) for d in description
        ]
        if len(price) > 1:
            product_price = [ProductPriceData(
                id=p.id, price=p.price, name=[ProductPriceNameData(
                    name=n.name, language=n.language,
                ) for n in p.name]) for p in price]
        else:
            product_price = [ProductPriceData(id=p.id, price=p.price, name=[]) for p in price]
        formatted_name = self.format(ExistingTypes.Text).format_product_names(product_name)
        formatted_description = self.format(ExistingTypes.Text).format_product_descriptions(product_description)
        if formatted_description != "":
            formatted_description += "\n\n"
        formatted_price = self.format(ExistingTypes.Text).format_product_prices(product_price)
        return (
            f"{formatted_name}\n\n"
            f"{formatted_description}"
            f"{formatted_price}"
        )

    def price_must_be_integer(self) -> str:
        return "Нужно ввести число"

    def list_is_empty(self) -> str:
        return "Список пуст"

    def change_menu_product_status_call_answer(self, status: MenuProductStatus) -> str:
        if status == MenuProductStatus.available:
            return "✅ Теперь продукт в наличии"
        else:
            return "⛔️ Теперь продукта нет в наличии"

    def access_delete_product(self) -> str:
        return "Вы подтверждаете удаление продукта?"

    # user
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
            f"\n\n<b>Итого  — {self.format(ExistingTypes.Text).format_product_price(total_amount)} сум</b>"
            f"\n\nХорошего дня!"
        )

    def send_finish_order_presentation_shipping(
            self, order_id: OrderId, products: list[ReadUserOrderProduct],
            shipping_amount: int, total_amount: int,
    ) -> str:
        return (
            f"Ваш заказ принят и будет отправлен в указанный срок. Номер вашего заказа #{order_id}.\n"
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
            first_name: str, phone: str, payment_type: type[ConcretePaymentTypeRu], address: str, comment: str,
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
        return f"Заказ #{order_id} в процессе приготовления.\nРасчетное время доставки от 40 минут."

    def wrong_phone_number(self) -> str:
        return ("⛔️ Неверно введен номер телефона, попробуйте снова. "
                "Отправьте или введите ваш номер телефона\nв формате: +998** *** ** **")

    def wrong_comment_length(self) -> str:
        return "⛔️ Слишком длинный комментарий, пожалуйста опишите то что вы хотите более кратко"

    def no_comment(self) -> str:
        return "Комментариев нет"