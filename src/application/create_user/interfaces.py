from src.application.common.interfaces import CreateUser, Committer


class DbGateway(CreateUser, Committer):
    pass
