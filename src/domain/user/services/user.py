from typing import Optional

from src.domain.user.constants.user import Member, Language
from src.domain.user.entities.user import User


class UserService:
    def create_user(self, name: str, phone: Optional[str], member: Member, language: Language) -> User:
        return User(id=None, name=name[:30], phone=phone, member=member, language=language)

    def edit_phone(self, phone: str, user: User) -> User:
        user.phone = phone
        return user

    def edit_language(self, language: Language, user: User) -> User:
        user.language = language
        return user

    def edit_user_name(self, name: str, user: User) -> User:
        user.name = name[:30]
        return user

    def promote_user(self, member: Member, user: User) -> User:
        user.member = member
        return user
