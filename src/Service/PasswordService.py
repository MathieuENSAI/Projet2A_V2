import hashlib
import secrets
from typing import Optional

def hash_password(pass_word: str, salt: Optional[str] = None) -> str:
    if salt is None:
        raise Exception("salt not found")
    return hashlib.sha256(salt.encode() + pass_word.encode()).hexdigest()


def create_salt() -> str:
    return secrets.token_hex(128)


def check_password_strength(pass_word: str):
    if len(pass_word) < 8:
        raise Exception("Password length must be at least 8 characters")
    if not any(char.isdigit() for char in pass_word):
        raise ValueError("Password must contain at least one number")
    if not any(char.isupper() for char in pass_word):
        raise ValueError("Password must contain at least one uppercase letter")
    if not any(char.islower() for char in pass_word):
        raise ValueError("Password must contain at least one lowercase letter")


def validate_password_salt(pass_word: str, hashed_password:str, salt:str) -> Optional[bool]:
    tested_password = hash_password(pass_word, salt)
    if tested_password != hashed_password:
        raise Exception("Password incorect")
    return True