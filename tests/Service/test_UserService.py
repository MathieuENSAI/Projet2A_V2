from unittest.mock import MagicMock
import pytest
from src.DAO.UserRepo import UserRepo
from src.Service.UserService import UserService
from src.Model.User import User
from src.Model.APIUser import APIUser
import src.Service.PasswordService as PasswordService


@pytest.fixture
def user_service():
    """Fixture pour simuler UserRepo et UserService"""
    user_repo=MagicMock(UserRepo)
    pass_word_service = MagicMock(PasswordService)
    return UserService(user_repo, pass_word_service), user_repo, pass_word_service

def test_create_user(user_service):
    user_service, user_repo, pass_word_service= user_service
    # Simulation des données
    username, pass_word="Yatoute", "Yatoute123"
    salt = "857eb4f7ede250d32b022b84d1ab7d498a929765aa4778f6badbc93e8a1ecfd18b41bd0cc16a7fe7d1f9af943759967c933362ab37d7450b1305511289aff1dfa4f4329341f84a12ae68c73bcb4f84857ccfe3acfa1d77f400ce0de5541d630daa2306d43368879a49719ef0ca885c9d994d2c8c1c1e89be363f86c5d2f3e09e"
    pass_word_service.create_salt.return_value=salt
    hashed_password = pass_word_service.hash_password(pass_word, salt)
    expected_user= APIUser(id_user=2, username=username)
    
    # Configuration des mocks
    user_repo.insert_into_db.return_value = expected_user

    # Appel de la méthode
    result = user_service.create_user(username, pass_word)

    # Vérifications
    user_repo.insert_into_db.assert_called_once_with(username = username, salt = salt, hashed_password=hashed_password)
    assert result == expected_user

def test_login_is_ok(user_service):
    user_service, user_repo, pass_word_service= user_service
    # Simulation des données
    id_user=2
    pass_word="Yatoute123"
    username ="Yatoute"
    hashed_password = "9f3b9bcf7b06c8241dc7caa55c36de4e5a2161d697f2a303a53ba707783c42a6"
    salt="5c6cf48d4003d3c5c7de4791b32385d114b211d2b1bd387803f1dbb5603b57bd1c4234367d9d6daa9dc22c84c60caeeacb87f2c98eadbfacaf366bb4b36ae0723c0f0fdb1ba51c5e059d4aa1bcaf9c814cfcdb72fbf78ce246c01e4cbb9cab1d255f8790135f070d6429365dc6f2113149bc74202705f281d01981c384790e37"
    expected_user = User(id_user=id_user, username=username, pass_word=hashed_password, salt=salt)
    user_repo.get_by_username.return_value = expected_user
    resultat =user_service.login(username, pass_word)
    assert resultat==expected_user

def test_login_username_incorect(user_service):
    user_service, user_repo, pass_word_service= user_service
    user_repo.get_by_username.return_value = None
    with pytest.raises(Exception, match="Username incorect"):
        user_service.login("Akouvi", "Akouvi123")

def test_login_password_incorect(user_service):
    user_service, user_repo, pass_word_service= user_service
    # Simulation des données
    id_user=2
    pass_word="Yatoute000"
    username ="Yatoute"
    hashed_password = "9f3b9bcf7b0lmùzzzzzeeeza56c8241dc7caa55c36de4e5a2161d697f2a303a53ba707783c42a6"
    salt="5c6cf48d4003d3c5c7de4791b32385d114b211d2b1bd387803f1dbb5603b57bd1c4234367d9d6daa9dc22c84c60caeeacb87f2c98eadbfacaf366bb4b36ae0723c0f0fdb1ba51c5e059d4aa1bcaf9c814cfcdb72fbf78ce246c01e4cbb9cab1d255f8790135f070d6429365dc6f2113149bc74202705f281d01981c384790e37"
    expected_user = User(id_user=id_user, username=username, pass_word=hashed_password, salt=salt)
    user_repo.get_by_username.return_value = expected_user
    pass_word_service.validate_password_salt.return_value = Exception
    resultat =user_service.login(username, pass_word)
    assert resultat==expected_user


def test_get_user_by_id(user_service):
    user_service, user_repo, _= user_service
    # Simulation des données
    id_user, username=2, "Yatoute"
    expected_user= APIUser(id_user=id_user, username=username)
    
    # Configuration des mocks
    user_repo.get_by_id.return_value = expected_user

    # Appel de la méthode
    result = user_service.get_user_by_id(id_user)

    # Vérifications
    user_repo.get_by_id.assert_called_once_with(id_user)
    assert result == expected_user

def test_get_user_by_username(user_service):
    user_service, user_repo, _= user_service
    # Simulation des données
    id_user, username=2, "Yatoute"
    expected_user= User(id_user=id_user, username=username)
    
    # Configuration des mocks
    user_repo.get_by_username.return_value = expected_user

    # Appel de la méthode
    result = user_service.get_user_by_username(username=username)

    # Vérifications
    user_repo.get_by_username.assert_called_once_with(username=username)
    assert result == expected_user

