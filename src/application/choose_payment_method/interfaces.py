from src.application.common.interfaces import ChoosePaymentMethod, GetOrder


class DbGateway(ChoosePaymentMethod, GetOrder):
    pass
