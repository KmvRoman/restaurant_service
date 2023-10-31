from src.application.common.interfaces import EditUserLanguage, GetUser, Committer


class DbGateway(EditUserLanguage, GetUser, Committer):
    pass
