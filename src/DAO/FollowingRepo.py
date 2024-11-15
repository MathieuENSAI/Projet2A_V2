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
            VALUES (%(id_user)s, %(id_following)s)
            ON CONFLICT (id_user, id_following) DO NOTHING;
            SELECT id_user, username FROM projet_info.User
            WHERE id_user=%(id_following)s;
            """
        try:
            following_add = self.db_connector.sql_query(query,{"id_user":id_user, "id_following":id_following},"one",)
        except ForeignKeyViolation:
            return None
        return APIUser(id=following_add["id_user"], username=following_add["username"])
    
    def is_user_follow(self, id_user:int, id_following:int):
        query="""
            SELECT * FROM projet_info.userfollowing
            WHERE id_user = %s AND id_following=%s;
        """
        following = self.db_connector.sql_query(query,(id_user, id_following),"one")
        return  True if following else False

    def get_all_following(self, id_user: int) -> list[APIUser]:
        query = """
            SELECT * FROM projet_info.user U
            JOIN projet_info.userfollowing UF ON U.id_user = UF.id_user
            WHERE U.id_user = %s;
            """
        raw_users = self.db_connector.sql_query(query, [id_user], "all" )
        return [APIUser(id=raw_user["id_following"], username=raw_user["username"]) for raw_user in raw_users]
    
    def get_following_seen_movies(self, id_following:int):

        query = """
        SELECT M.*, SM.vote AS following_vote, SM.favorite AS following_favorite FROM projet_info.SeenMovies SM
        JOIN projet_info.Movie M ON SM.id_movie=M.id
        WHERE SM.seen=TRUE AND SM.id_user=%s;
        """
        raws_collection = self.db_connector.sql_query(query, [id_following], "all" )
        return raws_collection
    
    def get_movies_seen_together(self, id_user:int, id_following:int):
        query = """
            SELECT M.*, SM2.vote AS following_vote, SM2.favorite AS following_favorite FROM projet_info.Movie M
            JOIN  projet_info.SeenMovies SM1 ON SM1.id_movie=M.id
            JOIN projet_info.SeenMovies SM2 ON SM1.id_movie = SM2.id_movie
            WHERE SM1.seen=TRUE AND SM2.seen=TRUE AND 
            SM1.id_user=%(id_user)s AND SM2.id_user=%(id_following)s     
        """
        raws_collection = self.db_connector.sql_query(query, {"id_user":id_user, "id_following":id_following}, "all" )
        return raws_collection
    
    def get_movies_liked_by_all_following(id_user:int):
        query="""
            SELECT * FROM projet_info.User
            JOIN projet_info.
        """
        return 0
    
    def get_top_movies_liked_by_all_following(id_user:int, top:int):
        return 0

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
    print(following_repo.add_following(1,3))