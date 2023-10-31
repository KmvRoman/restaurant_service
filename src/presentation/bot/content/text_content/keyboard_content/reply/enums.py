from dataclasses import dataclass
from enum import Enum


class MainMenu(str, Enum):
    menu: str
    info: str
    review: str
    settings: str


class MainMenuRu(MainMenu):
    menu = "🍽 Меню"
    info = "ℹ Информация"
    review = "✍ Оставить отзыв"
    settings = "⚙ Настройки"


class MainMenuUz(MainMenu):
    menu = "🍽 Menu"
    info = "ℹ Informatsiya"
    review = "✍ Otziv qoldirish"
    settings = "⚙ Nastroyka"


class Home(str, Enum):
    home: str


class HomeRu(Home):
    home = "🏠 Главное меню"


class HomeUz(Home):
    home = "🏠 Uiga"


class AdminHome(str, Enum):
    home: str


class AdminHomeRu(AdminHome):
    home = "Главное меню"


class AdminHomeUz(AdminHome):
    home = "Uiga"


class AdminMainMenu(str, Enum):
    menu: str
    newsletter: str
    upload_product: str
    statistic: str
    promotion: str


class AdminMainMenuRu(AdminMainMenu):
    menu = "Меню администратор"
    newsletter = "Рассылка"
    upload_product = "Загрузить товар"
    statistic = "Статистика"
    promotion = "Акции"


class ChooseOrderType(str, Enum):
    pickup: str
    shipping: str


class ChooseOrderTypeRu(ChooseOrderType):
    pickup = "🚶 Самовывоз"
    shipping = "🛵 Доставка"


class ChooseOrderTypeUz(ChooseOrderType):
    pickup = "🚶 Самовывоз"
    shipping = "🛵 Доставка"


class Back(str, Enum):
    back: str


class BackRu(Back):
    back = "⬅️ Назад"


class BackUz(Back):
    back = "⬅️ Otkazish"


class Skip(str, Enum):
    skip: str


class SkipRu(Skip):
    skip = "⏩ Пропустить"


class SkipUz(Skip):
    skip = "⏩ Otkazish"


class SendLocation(str, Enum):
    location: str


class SendLocationRu(SendLocation):
    location = "📍 Отправить локацию"


class SendLocationUz(SendLocation):
    location = "📍 Отправить локацию"


class WebApp(str, Enum):
    webapp: str


class WebAppRu(WebApp):
    webapp = "🍽 Перейти в меню"


class WebAppUz(WebApp):
    webapp = "🍽 Перейти в меню"


class MyPhoneNumber(str, Enum):
    phone: str


class MyPhoneNumberRu(MyPhoneNumber):
    phone = "📱 Мой номер"


class MyPhoneNumberUz(MyPhoneNumber):
    phone = "📱 Мой номер"


class Accept(str, Enum):
    accept: str


class AcceptRu(Accept):
    accept = "✅ Подтвердить"


class AcceptUz(Accept):
    accept = "✅ Подтвердить"


class PaymentTypes(str, Enum):
    cache: str
    payme: str
    click: str


class PaymentTypesRu(PaymentTypes):
    cache = "💵 Наличными"
    payme = "💳 Payme"
    click = "💳 Click"


class PaymentTypesUz(PaymentTypes):
    cache = "💵 Наличными"
    payme = "💳 Payme"
    click = "💳 Click"
