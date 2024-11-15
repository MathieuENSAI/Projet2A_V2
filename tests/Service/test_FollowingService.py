import pytest
from unittest.mock import MagicMock
from src.DAO.FollowingRepo import FollowingRepo
from src.DAO.UserRepo import UserRepo
from src.Model.User import User
from src.Service.FollowingService import FollowingService  

@pytest.fixture
def following_service():
    # Création des mocks pour FollowingRepo et UserRepo
    following_repo_mock = MagicMock(spec=FollowingRepo)
    user_repo_mock = MagicMock(spec=UserRepo)
    # Instanciation de FollowingService avec les mocks
    return FollowingService(following_repo=following_repo_mock, user_repo=user_repo_mock), following_repo_mock, user_repo_mock

def test_get_all_following(following_service):
    service, following_repo_mock, _ = following_service
    # Simuler un retour pour la méthode get_all_following
    following_repo_mock.get_all_following.return_value = [
        User(id=2, username="user2"),
        User(id=3, username="user3")
    ]
    
    result = service.get_all_following(1)
    
    # Vérifier que la méthode de FollowingRepo a bien été appelée avec le bon user_id
    following_repo_mock.get_all_following.assert_called_once_with(1)
    # Vérifier le résultat
    assert result == [
        User(id=2, username="user2"),
        User(id=3, username="user3")
    ]

def test_add_scout(following_service):
    service, following_repo_mock, _ = following_service
    user = User(id=1, username="user1")
    scout = User(id=2, username="scoutuser")
    
    service.add_scout(user, scout)
    
    # Vérifier que la méthode add_scout de FollowingRepo a bien été appelée avec les bons arguments
    following_repo_mock.add_scout.assert_called_once_with(user, scout)

def test_remove_scout(following_service):
    service, following_repo_mock, _ = following_service
    user = User(id=1, username="user1")
    scout = User(id=2, username="scoutuser")
    
    service.remove_scout(user, scout)
    
    # Vérifier que la méthode remove_scout de FollowingRepo a bien été appelée avec les bons arguments
    following_repo_mock.remove_scout.assert_called_once_with(user, scout)
