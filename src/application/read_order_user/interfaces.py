from src.application.common.interfaces import ReadOrderForUser, ReadOrderProductForUser


class DbGateway(ReadOrderForUser, ReadOrderProductForUser):
    pass
