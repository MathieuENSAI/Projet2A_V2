from typing import Optional

from src.Model.User import User

from .DBConnector import DBConnector

class FollowingRepo:
    db_connector: DBConnector

    def __init__(self, db_connector: DBConnector) -> None:
        self.db_connector = db_connector
    def retrieve_scouts(self, user: User) -> list[User]:
        raw_users = self.db_connector.sql_query(
            """
            SELECT * FROM users
            WHERE scout = %(scout)s;
            """,
            {"scout": user.id},
            "all",
        )
        if raw_users is None:
            return None
        return [User(**raw_user) for raw_user in raw_users]
    
    def add_scout(self, user: User, scout: User) -> User:
        raw_modified_user = self.db_connector.sql_query(
            """
            UPDATE users
            SET scout = %(scout)s
            WHERE id = %(id)s
            RETURNING *;
            """,
            {"scout": scout.id, "id": user.id},
            "one",
        )
        return User(**raw_modified_user)
    
    def remove_scout(self, user: User) -> User:
        raw_modified_user = self.db_connector.sql_query(
            """
            UPDATE users
            SET scout = NULL
            WHERE id = %(id)s
            RETURNING *;
            """,
            {"id": user.id},
            "one",
        )
        return User(**raw_modified_user)



    