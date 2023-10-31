from src.application.common.interfaces import AcceptOrder, GetOrder, Committer


class DbGateway(AcceptOrder, GetOrder, Committer):
    pass
