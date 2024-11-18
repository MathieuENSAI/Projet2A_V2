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
        return APIUser(**following_add)
    
    def delete_following(self, id_user:int, id_following:int):
        raw_delete = self.db_connector.sql_query(
            """DELETE FROM projet_info.UserFollowing WHERE id_user=%s AND id_following=%s;""",
            (id_user, id_following), "none"

        )
        return True if raw_delete else False
    
    def is_user_follow(self, id_user:int, id_following:int):
        query="""
            SELECT * FROM projet_info.userfollowing
            WHERE id_user = %s AND id_following=%s;
        """
        following = self.db_connector.sql_query(query,(id_user, id_following),"one")
        return  True if following else False

    def get_all_following(self, id_user: int) -> list[APIUser]:
        query = """
            SELECT U.* FROM projet_info.user U
            JOIN projet_info.userfollowing UF ON U.id_user = UF.id_user
            WHERE U.id_user = %s;
            """
        raw_users = self.db_connector.sql_query(query, [id_user], "all" )
        return [APIUser(**raw_user) for raw_user in raw_users]
    
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
    
    def get_movies_seen_by_all_following(self, id_user:int):
        query = """
        SELECT M.*, AVG(SM.vote) AS following_vote_average, 
        COUNT(CASE WHEN SM.favorite=TRUE THEN 1 END) AS total_liked_following
        FROM projet_info.Movie M
        JOIN projet_info.SeenMovies SM ON M.id=SM.id_movie
        JOIN projet_info.UserFollowing UF ON SM.id_user=UF.id_following AND UF.id_user=%s
        GROUP BY M.id
        ORDER BY following_vote_average DESC NULLS LAST, total_liked_following DESC;
        """
        raws_collection = self.db_connector.sql_query(query, [id_user], "all" )
        
        return raws_collection
    
    def get_movies_liked_by_all_following(self, id_user:int):
        query = """
        SELECT M.*, AVG(SM.vote) AS following_vote_average, 
        COUNT(CASE WHEN SM.favorite=TRUE THEN 1 END) AS total_liked_following
        FROM projet_info.Movie M
        JOIN projet_info.SeenMovies SM ON M.id=SM.id_movie
        JOIN projet_info.UserFollowing UF ON SM.id_user=UF.id_following AND UF.id_user=%s
        GROUP BY M.id
        HAVING COUNT(CASE WHEN SM.favorite = TRUE THEN 1 END) > 0
        ORDER BY total_liked_following DESC, following_vote_average DESC NULLS LAST;
        """
        raws_collection = self.db_connector.sql_query(query, [id_user], "all" )
        
        return raws_collection
    
    def get_new_follow_suggestion(self, id_user:int):
        query = """
        SELECT U.id_user, U.username, COUNT(SM1.id_movie) AS common_favorite_movies
        FROM projet_info.SeenMovies SM1
        JOIN projet_info.SeenMovies SM2 
        ON SM1.id_movie=SM2.id_movie AND SM2.id_user!= %(id_user)s AND SM2.favorite=TRUE 
        LEFT JOIN projet_info.UserFollowing UF 
        ON SM2.id_user=UF.id_following AND UF.id_user=%(id_user)s
        JOIN projet_info.User U
        ON SM2.id_user = U.id_user
        WHERE SM1.id_user =%(id_user)s AND SM1.favorite=TRUE
        AND UF.id_following IS NULL
        GROUP BY U.id_user
        ORDER BY common_favorite_movies DESC LIMIT 1;
        """
        raws_selected= self.db_connector.sql_query(query, {'id_user':id_user}, "one" )
        return raws_selected

    
    
        
if __name__ == "__main__" :
    import dotenv
    dotenv.load_dotenv()
    db_connector = DBConnector()
    following_repo = FollowingRepo(db_connector)
    print(following_repo.get_movies_liked_by_all_following(2))