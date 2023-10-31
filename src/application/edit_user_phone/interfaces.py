from src.application.common.interfaces import EditUserPhone, GetUser, Committer


class DbGateway(EditUserPhone, GetUser, Committer):
    pass
