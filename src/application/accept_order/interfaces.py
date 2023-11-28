from src.application.common.interfaces import AcceptOrder, ExistOrder, Committer


class DbGateway(AcceptOrder, ExistOrder, Committer):
    pass
