from src.application.common.interfaces import PromoteUser, GetUser, Committer


class DbGateway(PromoteUser, GetUser, Committer):
    pass
