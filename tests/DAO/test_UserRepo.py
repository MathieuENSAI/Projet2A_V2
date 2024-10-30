from typing import TYPE_CHECKING, Literal, Optional, Union

from src.DAO.UserRepo import UserRepo

if TYPE_CHECKING:
    from src.Model.User import User


class MockDBConnector:
    def sql_query(
        self,
        query: str,
        data: Optional[Union[tuple, list, dict]] = None,
        return_type: Union[Literal["one"], Literal["all"]] = "one",
    ):
        match query:
            case "SELECT * from user WHERE id=%s":
                if not data:
                    raise Exception
                id_user = data[0]
                return {"id_user": id_user, "username": "janjak", "pass_word": "myHashedPassword", "salt": "mySalt"}


def test_get_user_by_id():
    user_repo = UserRepo(MockDBConnector())
    user: User = user_repo.get_by_id(1)
    assert user is not None
    assert user.id == 1
    assert user.username == "janjak"