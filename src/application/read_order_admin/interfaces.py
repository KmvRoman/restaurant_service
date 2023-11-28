from src.application.common.interfaces import ReadOrderForAdmin, ReadOrderProductForAdmin


class DbGateway(ReadOrderForAdmin, ReadOrderProductForAdmin):
    pass
