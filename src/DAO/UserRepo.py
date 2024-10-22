from typing import Optional

from src.Model.User import User

from .DBConnector import DBConnector


class UserRepo:
    db_connector: DBConnector

    def __init__(self, db_connector: DBConnector):
        self.db_connector = db_connector

    def get_by_id(self, user_id: int) -> Optional[User]:
        raw_user = self.db_connector.sql_query("SELECT * from users WHERE id=%s", [user_id], "one")
        if raw_user is None:
            return None
        return User(**raw_user)

    def get_by_username(self, username: str) -> Optional[User]:
        raw_user = self.db_connector.sql_query("SELECT * from users WHERE username=%s", [username], "one")
        if raw_user is None:
            return None
        return User(**raw_user)

    def insert_into_db(self, username: str, salt: str, hashed_password: str) -> User:
        raw_created_user = self.db_connector.sql_query(
            """
        INSERT INTO users (id, username, salt, password)
        VALUES (DEFAULT, %(username)s, %(salt)s, %(password)s)
        RETURNING *;
        """,
            {"username": username, "salt": salt, "password": hashed_password},
            "one",
        )

        return User(**raw_created_user)

    def get_all(self) -> list[User]:
        raw_users = self.db_connector.sql_query("SELECT * from users", [], "all")
        if raw_users is None:
            return None
        return User(**raw_users)
    
    def modify_user(self, user: User) -> User:
        raw_modified_user = self.db_connector.sql_query(
            """
        UPDATE users
        SET username = %(username)s, salt = %(salt)s, password = %(password)s
        WHERE id = %(id)s
        RETURNING *;
        """,
            user.to_dict(),
            "one",
        )
        return User(**raw_modified_user)
    
    def delete_user(self, user: User) -> None:
        try:
            self.db_connector.sql_query(
                """
            DELETE FROM users
            WHERE id = %(id)s;
            """,
                user.to_dict(),
                "none",
            )
        except Exception as e:
            print(f"Error deleting user: {e}")
            raise e

    def login(self, username: str, password: str) -> Optional[User]:
        raw_user = self.db_connector.sql_query(
            """
            SELECT * FROM users
            WHERE username = %(username)s AND password = %(password)s;
            """,
            {"username": username, "password": password},
            "one",
        )
        if raw_user is None:
            return None
        return User(**raw_user)

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

