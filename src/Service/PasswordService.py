import hashlib
import secrets
from typing import Optional

from src.DAO.UserRepo import UserRepo
from src.Model.User import User


def hash_password(password: str, salt: Optional[str] = None) -> str:
    if salt is None:
        raise Exception("salt not found")
    return hashlib.sha256(salt.encode() + password.encode()).hexdigest()


def create_salt() -> str:
    return secrets.token_hex(128)


def check_password_strength(password: str):
    if len(password) < 8:
        raise Exception("Password length must be at least 8 characters")


def validate_username_password(username: str, password: str, user_repo: UserRepo) -> User:
    user_with_username: Optional[User] = user_repo.get_by_username(username=username)
    user = UserRepo.get_by_username(username)
    tested_password = hash_password(password, user.salt)
    if tested_password != user(pass_word):
        raise Exception("Incorrect Password")
    ##J'ai fais ça, jsp si c'est bon (à revoir en fction du reste)
    return user_with_username
