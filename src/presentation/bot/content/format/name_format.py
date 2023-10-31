from src.application.read_current_basket.dto import PreparedBasketProduct
from src.domain.user.constants.user import Language
from src.presentation.bot.content.content_enums import ExistingTypes
from src.presentation.bot.content.text_content.interfaces import IFormat
from src.presentation.bot.states.state_data.product import ProductNameData, ProductDescriptionData, ProductPriceData


class TextFormat(IFormat):
    format = ExistingTypes.Text

    def number_to_emoji(self, number: int) -> str:
        response = ""
        emojis = ["0️⃣", "1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣"]
        number_in_str = str(number)
        for num in number_in_str:
            response += emojis[int(num)]
        return response

    def format_product_names(self, names: list[ProductNameData]) -> str:
        string = ""
        for name in names:
            string += f"<b>{name.name}</b> ({name.language}), "
        else:
            string = string[0:-2]
            string += "."
        return string

    def format_product_descriptions(self, descriptions: list[ProductDescriptionData]) -> str:
        string = ""
        for description in descriptions:
            string += f"<i>{description.description}</i> ({description.language})\n"
        if string != "":
            string = string[0:-1]
        return string

    def format_product_prices(self, prices: list[ProductPriceData]) -> str:
        if len(prices) == 1 and len(prices[0].name) == 0:
            return f"<b>{self.format_product_price(obj=prices[0].price)} сум</b>"
        string = ""
        for count, price in enumerate(prices):
            if count == 0:
                string += f"<b>{self.format_product_price(obj=price.price)} сум </b> ("
            else:
                string += f"\n<b>{self.format_product_price(obj=price.price)} сум </b> ("
            for price_name in price.name:
                string += f"{price_name.name} ({price_name.language}), "
            else:
                string = string[0:-2]
                string += ")"
        return string

    def format_product_price(self, obj: int) -> str:
        return "{0:,}".format(obj).replace(",", " ")

    def format_products_view(self, products: list[PreparedBasketProduct], currency_name: str) -> str:
        string = ""
        for product in products:
            if product.modification is None:
                string += (
                    f"\n<b>{product.name}</b>\n"
                    f"{self.number_to_emoji(number=product.count)} ✖️ "
                    f"{self.format_product_price(obj=product.price)} — "
                    f"<b>{self.format_product_price(obj=product.amount)} {currency_name}</b>"
                )
            else:
                string += (
                    f"\n<b>{product.name}</b> ({product.price_name})\n"
                    f"{self.number_to_emoji(number=product.count)} ✖️ "
                    f"{self.format_product_price(obj=product.price)} — "
                    f"<b>{self.format_product_price(obj=product.amount)} {currency_name}</b>"
                )
        return string

    def format_products_view_admin(self, products: list[PreparedBasketProduct]) -> str:
        string = ""
        for product in products:
            if product.modification is None:
                string += f"\n{product.name} — {product.count} шт."
            else:
                string += f"\n{product.name} ({product.price_name}) шт."
        return string
