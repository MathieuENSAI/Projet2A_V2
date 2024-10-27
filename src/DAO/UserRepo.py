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
    
    def modify_user(self, last_username, user: User) -> User:
        raw_modified_user = self.db_connector.sql_query(
        "UPDATE projet_info.User SET username = %(username)s, salt = %(salt)s, pass_word = %(pass_word)s WHERE username = %(last_username)s RETURNING *;",
            {"username": user.username, "salt": user.salt, "pass_word": user.pass_word, "last_username" : last_username},
            "one",
        )
        return User(**raw_modified_user)
    
    def delete_user(self, username:str) -> None:
        try:
            self.db_connector.sql_query(
                """
            DELETE FROM projet_info.User
            WHERE username = %s;
            """,
                (username,),
                "none",
            )
        except Exception as e:
            print(f"Error deleting user: {e}")
            raise e

    def login(self, username: str, pass_word: str) -> Optional[User]:
        raw_user = self.db_connector.sql_query(
            """
            SELECT * FROM projet_info.User
            WHERE username = %(username)s AND pass_word = %(pass_word)s;
            """,
            {"username": username, "pass_word": pass_word},
            "one",
        )
        if raw_user is None:
            return None
        return User(**raw_user)

    # def retrieve_scouts(self, user: User) -> list[User]:
    #     raw_users = self.db_connector.sql_query(
    #         """
    #         SELECT * FROM User
    #         WHERE scout = %(scout)s;
    #         """,
    #         {"scout": user.id_user},
    #         "all",
    #     )
    #     if raw_users is None:
    #         return None
    #     return [User(**raw_user) for raw_user in raw_users]

if __name__ == "__main__" :
    import dotenv
    dotenv.load_dotenv()
    db_connector = DBConnector()
    user_repo = UserRepo(db_connector)
    # Tester une méthode de user_repo
  
    
   
