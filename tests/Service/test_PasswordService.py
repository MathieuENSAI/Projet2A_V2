from typing import Optional

import pytest

from src.Model.User import User
from src.Service.PasswordService import create_salt, hash_password, validate_password_salt, check_password_strength


def test_hash_password_salt_no_found():
    password = "soleil1234"
    with pytest.raises(Exception, match="salt not found"):
        hashed_password = hash_password(password)

def test_hash_password_with_salt():
    password = "soleil1234"
    salt = "jambon"
    hashed_password = hash_password(password, salt)
    assert hashed_password == "56d25b0190eb6fcdab76f20550aa3e85a37ee48d520ac70385ae3615deb7d53a"


def test_create_salt():
    salt = create_salt()
    assert len(salt) == 256

def test_check_password_strength_is_ok():
    password = "Yatoute1234"
    assert check_password_strength(password)==None

def test_check_password_strength_password_too_short():
    password = "Alex1"
    with pytest.raises(Exception, match="Password length must be at least 8 characters"):
        check_password_strength(password)

def test_check_password_strength_password_contain_no_number():
    password = "Yatouteaaaa"
    with pytest.raises(Exception, match="Password must contain at least one number"):
        check_password_strength(password)

def test_check_password_strength_password_contain_no_uppercase_letter():
    password = "yatoute123"
    with pytest.raises(Exception, match="Password must contain at least one uppercase letter"):
        check_password_strength(password)

def test_check_password_strength_password_contain_no_lowercase_letter():
    password = "YATOUTE123"
    with pytest.raises(Exception, match="Password must contain at least one lowercase letter"):
        check_password_strength(password)

def test_validate_password_salt_is_ok():
    pass_word="Yatoute123"
    hashed_password = "9f3b9bcf7b06c8241dc7caa55c36de4e5a2161d697f2a303a53ba707783c42a6"
    salt="5c6cf48d4003d3c5c7de4791b32385d114b211d2b1bd387803f1dbb5603b57bd1c4234367d9d6daa9dc22c84c60caeeacb87f2c98eadbfacaf366bb4b36ae0723c0f0fdb1ba51c5e059d4aa1bcaf9c814cfcdb72fbf78ce246c01e4cbb9cab1d255f8790135f070d6429365dc6f2113149bc74202705f281d01981c384790e37"
    resultat = validate_password_salt(pass_word, hashed_password, salt)
    assert resultat==True
    

def test_validate_password_salt_incorrect_password():
    pass_word="Emile123"
    hashed_password = "9f3b9bcf7b06c8241dc7caa55c36de4e5a2161d697f2a303a53ba707783c42a6"
    salt="5c6cf48d4003d3c5c7de4791b32385d114b211d2b1bd387803f1dbb5603b57bd1c4234367d9d6daa9dc22c84c60caeeacb87f2c98eadbfacaf366bb4b36ae0723c0f0fdb1ba51c5e059d4aa1bcaf9c814cfcdb72fbf78ce246c01e4cbb9cab1d255f8790135f070d6429365dc6f2113149bc74202705f281d01981c384790e37"
    with pytest.raises(Exception, match="Password incorect"):
        validate_password_salt(pass_word, hashed_password, salt)