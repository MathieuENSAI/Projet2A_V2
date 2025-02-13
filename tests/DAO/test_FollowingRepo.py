from typing import Literal, Optional, Union
from src.Model.APIUser import APIUser
from src.DAO.FollowingRepo import FollowingRepo
from psycopg2.errors import ForeignKeyViolation

class MockDBConnectorfollowing:
    def __init__(self):
        self.db = [
            {
                "id_user": 3,
                "username_user": "Jean-Jacques",
                "id_following": 1,
                "username_followed": "Emile"
            },
            {
                "id_user": 1,
                "username_user": "Emile",
                "id_following": 3,
                "username_followed": "Jean-Jacques"
            },
            {
                "id_user": 2,
                "username_user": "Jolerigolo",
                "id_following": 1,
                "username_followed": "Emile"
            },
            {
                "id_user": 4,
                "username_user": "numeroquatre",
                "id_following": 1,
                "username_followed": "Emile"
            },
            {
                "id_user": 3,
                "username_user": "Jean-Jacques",
                "id_following": 2,
                "username_followed": "Jolerigolo"
            },
        ]

    def sql_query(
        self,
        query: str,
        data: Optional[Union[tuple, list, dict]] = None,
        return_type: Union[Literal["one"], Literal["all"]] = "none",
    ):
        match query:
            case """
            INSERT INTO projet_info.userfollowing(id_user, id_following)
            VALUES (%(id_user)s, %(id_following)s)
            ON CONFLICT (id_user, id_following) DO NOTHING;
            SELECT id_user, username FROM projet_info.User
            WHERE id_user=%(id_following)s;
            """:
                id_user = data["id_user"]
                id_following = data["id_following"]

                for relation in self.db:
                    if relation["id_user"] == id_user and relation["id_following"] == id_following:
                        raise ForeignKeyViolation

                self.db.append({
                    "id_user": id_user,
                    "id_following": id_following,
                    "username_user": "",
                    "username_followed": ""
                })
                return {"id_user": id_following, "username": ""}


def test_add_following_success():
    followingrepo = FollowingRepo(MockDBConnectorfollowing())
    followed: APIUser = followingrepo.add_following(id_user=1, id_following=8)
    assert followed is not None
    assert followed == APIUser(id_user=8, username="")
    assert followingrepo.db_connector.db[-1]["id_user"] == 1
    assert followingrepo.db_connector.db[-1]["id_following"] == 8

def test_add_following_none():
    followingrepo = FollowingRepo(MockDBConnectorfollowing())
    followed: APIUser = followingrepo.add_following(id_user=1, id_following=3)
    assert followed is None

# def test_add_following_foreign_key_violation(following_repo):
#     repo, db_connector_mock = following_repo
#     # Simuler une violation de clé étrangère
#     db_connector_mock.sql_query.side_effect = ForeignKeyViolation
    
#     result = repo.add_following(1, 2)
    
#     assert result is False  # Vérifier que le retour est False en cas de ForeignKeyViolation

# def test_get_all_following(following_repo):
#     repo, db_connector_mock = following_repo
#     # Simuler un résultat de requête pour get_all_following
#     db_connector_mock.sql_query.return_value = [
#         {"id_following": 2, "username": "user2"},
#         {"id_following": 3, "username": "user3"},
#     ]
    
#     result = repo.get_all_following(1)
    
#     db_connector_mock.sql_query.assert_called_once_with(
#         """
#             SELECT * FROM projet_info.user U
#             JOIN projet_info.userfollowing UF ON U.id_user = UF.id_user
#             WHERE U.id_user = %s;
#             """,
#         [1],
#         "all",
#     )
#     # Vérifier que le résultat est une liste d'objets APIUser avec les bonnes données
#     assert result == [APIUser(id=2, username="user2"), APIUser(id=3, username="user3")]

# def test_remove_scout(following_repo):
#     repo, db_connector_mock = following_repo
#     # Simuler une réponse de la requête pour remove_scout
#     db_connector_mock.sql_query.return_value = {
#         "id": 1,
#         "username": "testuser",
#         "scout": None
#     }
    
#     user = User(id=1, username="testuser", scout=True)
#     result = repo.remove_scout(user)
    
#     db_connector_mock.sql_query.assert_called_once_with(
#         """
#             UPDATE users
#             SET scout = NULL
#             WHERE id = %(id)s
#             RETURNING *;
#             """,
#         {"id": 1},
#         "one",
#     )
#     # Vérifier que le résultat est bien un objet User modifié
#     assert result == User(id=1, username="testuser", scout=None)
