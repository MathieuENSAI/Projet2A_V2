import pytest
from unittest.mock import MagicMock
from psycopg2.errors import ForeignKeyViolation
from src.Model.User import User
from src.Model.APIUser import APIUser
from src.DAO.FollowingRepo import FollowingRepo
from src.DAO.DBConnector import DBConnector

# Fixture pour créer un objet FollowingRepo avec un DBConnector mocké
@pytest.fixture
def following_repo():
    db_connector_mock = MagicMock(spec=DBConnector)
    return FollowingRepo(db_connector=db_connector_mock), db_connector_mock

def test_add_following_success(following_repo):
    repo, db_connector_mock = following_repo
    # Simuler un résultat de succès pour sql_query
    db_connector_mock.sql_query.return_value = None
    
    result = repo.add_following(1, 2)
    
    db_connector_mock.sql_query.assert_called_once_with(
        """
            INSERT INTO projet_info.userfollowing(id_user, id_following)
            VALUES (%s, %s)
            ON CONFLICT (id_user, id_following) DO NOTHING;
            """,
        (1, 2),
        "none",
    )
    assert result is True  # Vérifier que le retour est True en cas de succès

def test_add_following_foreign_key_violation(following_repo):
    repo, db_connector_mock = following_repo
    # Simuler une violation de clé étrangère
    db_connector_mock.sql_query.side_effect = ForeignKeyViolation
    
    result = repo.add_following(1, 2)
    
    assert result is False  # Vérifier que le retour est False en cas de ForeignKeyViolation

def test_get_all_following(following_repo):
    repo, db_connector_mock = following_repo
    # Simuler un résultat de requête pour get_all_following
    db_connector_mock.sql_query.return_value = [
        {"id_following": 2, "username": "user2"},
        {"id_following": 3, "username": "user3"},
    ]
    
    result = repo.get_all_following(1)
    
    db_connector_mock.sql_query.assert_called_once_with(
        """
            SELECT * FROM projet_info.user U
            JOIN projet_info.userfollowing UF ON U.id_user = UF.id_user
            WHERE U.id_user = %s;
            """,
        [1],
        "all",
    )
    # Vérifier que le résultat est une liste d'objets APIUser avec les bonnes données
    assert result == [APIUser(id=2, username="user2"), APIUser(id=3, username="user3")]

def test_remove_scout(following_repo):
    repo, db_connector_mock = following_repo
    # Simuler une réponse de la requête pour remove_scout
    db_connector_mock.sql_query.return_value = {
        "id": 1,
        "username": "testuser",
        "scout": None
    }
    
    user = User(id=1, username="testuser", scout=True)
    result = repo.remove_scout(user)
    
    db_connector_mock.sql_query.assert_called_once_with(
        """
            UPDATE users
            SET scout = NULL
            WHERE id = %(id)s
            RETURNING *;
            """,
        {"id": 1},
        "one",
    )
    # Vérifier que le résultat est bien un objet User modifié
    assert result == User(id=1, username="testuser", scout=None)
