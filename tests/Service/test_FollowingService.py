import pytest
from unittest.mock import MagicMock
from src.DAO.FollowingRepo import FollowingRepo
from src.Model.APIUser import APIUser
from src.Service.FollowingService import FollowingService  

"""
Les tests du service FollowingService sont effectués pour vérifier que les méthodes services
appellent correctement les méthodes DAO de FollowingRepo et que les résultats renvoyés par 
les méthodes services sont effectivement ceux renvoyés par les méthodes DAO.

"""
@pytest.fixture
def following_service():
    """ Création de mocks pour FollowingRepo"""
    following_repo_mock = MagicMock(spec=FollowingRepo)
    return FollowingService(following_repo=following_repo_mock), following_repo_mock

def test_add_following(following_service):
    service, following_repo_mock = following_service
    resultat = service.add_following(1, 2)
    following_repo_mock.add_following.assert_called_once_with(1, 2)
    assert resultat == following_repo_mock.add_following.return_value

def test_stop_follow(following_service):
    service, following_repo_mock = following_service
    resultat = service.stop_follow(1, 2)
    following_repo_mock.delete_following.assert_called_once_with(1, 2)
    assert resultat == following_repo_mock.delete_following.return_value

def test_is_user_follow(following_service):
    service, following_repo_mock = following_service
    resultat = service.is_user_follow(1, 2)
    following_repo_mock.is_user_follow.assert_called_once_with(1, 2)
    assert resultat == following_repo_mock.is_user_follow.return_value
    
def test_get_all_following(following_service):
    service, following_repo_mock = following_service
    result = service.get_all_following(1)
    following_repo_mock.get_all_following.assert_called_once_with(1)
    assert result == following_repo_mock.get_all_following.return_value
    
def test_get_following_movies_collection(following_service):
    service, following_repo_mock = following_service
    result = service.get_following_movies_collection(1, 2)
    following_repo_mock.get_following_seen_movies.assert_called_once_with(2)
    following_repo_mock.get_movies_seen_together.assert_called_once_with(1, 2)
    assert result == {"following_seen_movies": following_repo_mock.get_following_seen_movies.return_value,
        "movies_seen_together": following_repo_mock.get_movies_seen_together.return_value}