import hashlib
import secrets
from typing import Optional

from src.DAO.UserRepo import UserRepo
from src.Model.User import User


def hash_password(pass_word: str, salt: Optional[str] = None) -> str:
    if salt is None:
        raise Exception("salt not found")
    return hashlib.sha256(salt.encode() + pass_word.encode()).hexdigest()


def create_salt() -> str:
    return secrets.token_hex(128)


def check_password_strength(pass_word: str):
    if len(pass_word) < 8:
        raise Exception("Password length must be at least 8 characters")


def validate_username_password(username: str, pass_word: str, user_repo: UserRepo) -> User:
    user_with_username: Optional[User] = user_repo.get_by_username(username=username)
    tested_password = hash_password(pass_word, user_with_username.salt)
    if tested_password != user_with_username.pass_word:
        raise Exception("Incorrect Password")
    return user_with_username
