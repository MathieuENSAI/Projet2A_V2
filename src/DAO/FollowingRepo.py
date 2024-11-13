from typing import Optional
from psycopg2.errors import ForeignKeyViolation
from src.Model.User import User
from src.Model.APIUser import APIUser

from src.DAO.DBConnector import DBConnector

class FollowingRepo:
    db_connector: DBConnector

    def __init__(self, db_connector: DBConnector) -> None:
        self.db_connector = db_connector

    def add_following(self, id_user: int, id_following: int) -> bool:
        query="""
            INSERT INTO projet_info.userfollowing(id_user, id_following)
            VALUES (%s, %s)
            ON CONFLICT (id_user, id_following) DO NOTHING;
            """
        try:
            raw_add = self.db_connector.sql_query(query,(id_user, id_following),"none",)
        except ForeignKeyViolation:
            return False
        return True
    
    def get_all_following(self, id_user: int) -> list[APIUser]:
        query = """
            SELECT * FROM projet_info.user U
            JOIN projet_info.userfollowing UF ON U.id_user = UF.id_user
            WHERE U.id_user = %s;
            """
        raw_users = self.db_connector.sql_query(query, [id_user], "all" )
        return [APIUser(id=raw_user["id_following"], username=raw_user["username"]) for raw_user in raw_users]
    
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

if __name__ == "__main__" :
    import dotenv
    dotenv.load_dotenv()
    db_connector = DBConnector()
    following_repo = FollowingRepo(db_connector)
    print(following_repo.add_following(4, 1))
    print(following_repo.get_all_following(5))