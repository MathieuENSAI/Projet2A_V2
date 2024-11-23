from typing import Optional

from src.Model.User import User

from src.DAO.DBConnector import DBConnector


class UserRepo:
    db_connector: DBConnector

    def __init__(self, db_connector: DBConnector):
        self.db_connector = db_connector

    def get_by_id(self, id_user: int) -> Optional[User]:
        raw_user = self.db_connector.sql_query("SELECT * from projet_info.User WHERE id_user=%s;", [id_user], "one")
        if raw_user is None:
            return None
        return User(**raw_user)

    def get_by_username(self, username: str) -> Optional[User]:
        raw_user = self.db_connector.sql_query("SELECT * from projet_info.User WHERE username=%s;", [username], "one")
        if raw_user is None:
            return None
        return User(**raw_user)

    def insert_into_db(self, username: str, salt: str, hashed_password: str) -> User:
        raw_created_user = self.db_connector.sql_query("INSERT INTO projet_info.User (id_user, username, salt, pass_word) VALUES (DEFAULT, %(username)s, %(salt)s, %(pass_word)s) RETURNING *;",
            {"username": username, "salt": salt, "pass_word": hashed_password},
            "one",
        )
        return User(**raw_created_user) if raw_created_user else None

    def get_all(self) -> list[User]:
        raw_users = self.db_connector.sql_query("SELECT * from projet_info.User;", [], "all")
        if raw_users is None:
            return None
        return [User(**raw_user) for raw_user in raw_users]
    
    def update_user(self, new_profile_user: User) -> User:
        raw_modified_user = self.db_connector.sql_query(
        "UPDATE projet_info.User SET username = %(username)s, salt = %(salt)s, pass_word = %(pass_word)s WHERE id_user = %(id_user)s RETURNING *;",
            {"id_user":new_profile_user.id_user, "username": new_profile_user.username, "salt": new_profile_user.salt, "pass_word": new_profile_user.pass_word},
            "one",
        )
        return User(**raw_modified_user)
    
    def delete_user(self, user_id:int) -> None:
        try:
            self.db_connector.sql_query(
                """
            DELETE FROM projet_info.User
            WHERE id_user = %s;
            """,
                [user_id],
                "none",
            )
        except Exception as e:
            return False
        return True

if __name__ == "__main__" :
    import dotenv
    dotenv.load_dotenv()
    db_connector = DBConnector()
    user_repo = UserRepo(db_connector)
    # Tester une méthode de user_repo
  
    
   
