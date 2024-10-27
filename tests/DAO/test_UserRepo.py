from typing import TYPE_CHECKING, Literal, Optional, Union
from src.DAO.UserRepo import UserRepo

if TYPE_CHECKING:
    from src.Model.User import User


class MockDBConnector:
    def __init__(self):
        self.db = [{"id_user": 1, "username": "user1", "salt": "mySalt1", "pass_word": "myHashedPassword1"}, 
            {"id_user": 2, "username": "user2", "salt": "mySalt", "pass_word": "myHashedPassword"},
            {"id_user": 3, "username": "user3", "salt": "mySalt", "pass_word": "myHashedPassword"}]

    def sql_query(
        self,
        query: str,
        data: Optional[Union[tuple, list, dict]] = None,
        return_type: Union[Literal["one"], Literal["all"]] = "none",
    ):
        match query:
            case "SELECT * from projet_info.User WHERE id_user=%s;":
                if not data:
                    raise Exception
                id_user = data[0]
                for user in self.db:
                    if user["id_user"] == id_user:
                        return user
                return None

            case "SELECT * from projet_info.User WHERE username=%s;":
                if not data:
                    raise Exception
                username = data[0]
                for user in self.db:
                    if user["username"] == username:
                        return user
                return None
                
            case "INSERT INTO projet_info.User (id_user, username, salt, pass_word) VALUES (DEFAULT, %(username)s, %(salt)s, %(pass_word)s) RETURNING *;":
                if not data:
                    raise Exception
                self.db.append({"id_user": len(self.db)+1, "username": data['username'], "salt": data['salt'], "pass_word": data['pass_word']})
                return(self.db[-1])
            case "SELECT * from projet_info.User;":
                return self.db


def test_get_user_by_id():
    user_repo = UserRepo(MockDBConnector())
    db = user_repo.db_connector.db
    user: User = user_repo.get_by_id(1)
    assert user is not None
    assert user.id_user == 1
    assert user.__dict__ == db[0] |{"following": [], "favorite_movie": [], "watchlist":[]}

def test_get_user_by_username():
    user_repo = UserRepo(MockDBConnector())
    db = user_repo.db_connector.db
    user: User = user_repo.get_by_username("user1")
    assert user is not None
    assert user.username == "user1"
    assert user.__dict__ == db[0] |{"following": [], "favorite_movie": [], "watchlist":[]}

def test_insert_into_db():
    user_repo = UserRepo(MockDBConnector())
    db = user_repo.db_connector.db
    user: User = user_repo.insert_into_db("Yatoute", "ajjdkkalelaleelser", "aaaaaselrlllzlrls")
    assert user is not None
    assert user.__dict__ == db[-1]|{"following": [], "favorite_movie": [], "watchlist":[]}
    assert user.username == "Yatoute"
    assert user.salt == "ajjdkkalelaleelser"
    assert user.pass_word == "aaaaaselrlllzlrls"
 
def test_get_all_users():
    user_repo = UserRepo(MockDBConnector())
    db = user_repo.db_connector.db
    users: list[User] = user_repo.get_all()
    assert users is not None
    assert users[0].__dict__== db[0]|{"following": [], "favorite_movie": [], "watchlist":[]}
    assert users[1].__dict__== db[1]|{"following": [], "favorite_movie": [], "watchlist":[]}
    assert users[2].__dict__== db[2]|{"following": [], "favorite_movie": [], "watchlist":[]}

