from src.application.common.interfaces import EditUserName, GetUser, Committer


class DbGateway(EditUserName, GetUser, Committer):
    pass
