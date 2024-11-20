from typing import Optional
from src.Model.SeenMovie import SeenMovie
from src.DAO.DBConnector import DBConnector
from src.Model.Movie import Movie
from src.Model.APIUser import APIUser


class SeenMovieRepo:
    db_connector: DBConnector

    def __init__(self, db_connector: DBConnector):
        self.db_connector = db_connector
    
    def get_by_user_and_movie(self, id_user: int, id_movie: int ) -> Optional[SeenMovie]:
        raw_seenmovie = self.db_connector.sql_query(
            """SELECT * from projet_info.seenmovies 
               WHERE id_user =%(id_user)s
               AND id_movie =%(id_movie)s;""",
               {"id_user":id_user, "id_movie":id_movie}, "one")
        if raw_seenmovie is None:
            return None
        return SeenMovie(**raw_seenmovie)

    def insert_into_db(self, id_user : int, id_movie : int, seen : bool=True, to_watch_later:bool=False, vote : int = None, favorite : bool = False) -> SeenMovie:
        raw_created_seenmovie = self.db_connector.sql_query(
                """INSERT INTO projet_info.seenmovies (id_user, id_movie, seen, to_watch_later, vote, favorite)
                VALUES (%(id_user)s, %(id_movie)s, %(seen)s, %(to_watch_later)s, %(vote)s, %(favorite)s)
                ON CONFLICT(id_user, id_movie) DO UPDATE
                SET seen = EXCLUDED.seen,
                    to_watch_later = EXCLUDED.to_watch_later,
                    vote = EXCLUDED.vote,
                    favorite = EXCLUDED.favorite
                RETURNING *;""",
                {"id_user": id_user, "id_movie": id_movie, "seen" : seen, "to_watch_later":to_watch_later, 
                 "vote" : vote, "favorite":favorite},"one")
        if raw_created_seenmovie is None:
            return None
        return SeenMovie(**raw_created_seenmovie)
    
    def update_db(self, seenmovie: SeenMovie):
        raw_update = self.db_connector.sql_query(
            """UPDATE projet_info.seenmovies
            SET seen = %(seen)s, 
                to_watch_later = %(to_watch_later)s,
                vote = %(vote)s,
                favorite = %(favorite)s
            WHERE id_user = %(id_user)s
            AND id_movie = %(id_movie)s;""",
            {
                "seen": seenmovie.seen,
                "to_watch_later" : seenmovie.to_watch_later,
                "vote": seenmovie.vote,
                "favorite": seenmovie.favorite,
                "id_user": seenmovie.id_user,
                "id_movie": seenmovie.id_movie
                },
                "none"
            )
        return True if raw_update else False
    
    def remove_from_user_favorites(self, id_user:int, id_movie:int):
        raw_update = self.db_connector.sql_query(
        """UPDATE projet_info.seenmovies
           SET favorite = FALSE
           WHERE id_user = %(id_user)s AND id_movie = %(id_movie)s;""",
            {
                "id_user": id_user,
                "id_movie": id_movie
                },
                "none"
            )
        return True if raw_update else False
    
    def remove_from_user_watchlist(self, id_user:int, id_movie:int):
        raw_update = self.db_connector.sql_query(
        """UPDATE projet_info.seenmovies
           SET to_watch_later = FALSE
           WHERE id_user = %(id_user)s AND id_movie = %(id_movie)s;""",
            {
                "id_user": id_user,
                "id_movie": id_movie
                },
                "none"
            )
        return True if raw_update else False
    
    
    def get_movies_seen_by_user(self, id_user : int) -> list[Movie]|None:
        """ Returns the list of movies id seen by a user"""
        raw_movies = self.db_connector.sql_query(
            """SELECT *
            FROM projet_info.seenmovies AS sm
            JOIN projet_info.movie AS m
            ON sm.id_movie = m.id
            WHERE sm.id_user = %(id_user)s
            AND sm.seen = TRUE;
            """,
            {"id_user": id_user}, "all",
        )
        if raw_movies:
            return [Movie(**raw_movie) for raw_movie in raw_movies]
        else:
            return None
        
    def get_watchlist_movie(self, id_user : int) -> list[Movie]|None:
        """ Returns the movies a user wanna see in the future"""
        raw_movies = self.db_connector.sql_query(
            """SELECT *
            FROM projet_info.seenmovies AS sm
            JOIN projet_info.movie AS m
            ON sm.id_movie = m.id
            WHERE sm.id_user = %(id_user)s
            AND sm.to_watch_later = TRUE;
            """,
            {"id_user": id_user}, "all",
        )
        if raw_movies:
            return [Movie(**raw_movie) for raw_movie in raw_movies]
        else:
            return None
        
    def get_user_favorites_movie(self, id_user : int) -> list[Movie]|None:
        """ Returns the list of favorite movies of an user"""
        raw_movies = self.db_connector.sql_query(
            """SELECT *
            FROM projet_info.seenmovies AS sm
            JOIN projet_info.movie AS m
            ON sm.id_movie = m.id
            WHERE sm.id_user = %(id_user)s
            AND sm.favorite = TRUE;
            """,
            {"id_user": id_user}, "all",
        )
        if raw_movies:
            return [Movie(**raw_movie) for raw_movie in raw_movies]
        else:
            return None
        
    def get_users_who_watch_movie(self, id_movie : int) -> list[APIUser]|None:
        """ Returns the list of users who have seen a movie"""
        raw_users = self.db_connector.sql_query(
            """SELECT *
            FROM projet_info.seenmovies AS sm
            JOIN projet_info.user AS m
            ON sm.id_user = m.id_user
            WHERE sm.id_movie = %(id_movie)s
            AND sm.seen = TRUE;
            """,
            {"id_movie": id_movie}, "all",
        )
        if raw_users:
            return [User(**raw_user) for raw_user in raw_users]
        else:
            return None
    
    def note_movie(self, id_user: int, id_movie: int, note: int):

        query = """
            INSERT INTO projet_info.seenmovies (id_user, id_movie, seen, favorite, vote, to_watch_later)
            VALUES (%(id_user)s, %(id_movie)s, TRUE, FALSE, %(vote)s, FALSE)
            ON CONFLICT (id_movie, id_user)
            DO UPDATE SET vote = EXCLUDED.vote, seen=TRUE;
            SELECT AVG(vote) AS vote_avg, COUNT(vote) AS vote_count 
            FROM projet_info.seenmovies
            WHERE id_movie = %(id_movie)s;"""
        vote_movie= self.db_connector.sql_query(query, {"id_user": id_user, "id_movie": id_movie, "vote": note}, "one")
        
        return vote_movie if vote_movie else None
    
    def remove_note_movie(self, id_user:int, id_movie:int):
        query = """
        UPDATE projet_info.SeenMovies
        SET vote=NULL
        WHERE id_user=%(id_user)s AND id_movie=%(id_movie)s;
        SELECT AVG(vote) AS vote_avg, COUNT(vote) AS vote_count 
            FROM projet_info.seenmovies
            WHERE id_movie = %(id_movie)s;
        """
        vote_movie = self.db_connector.sql_query(query, {"id_user": id_user, "id_movie": id_movie}, "one")
       
        return vote_movie if vote_movie else None

    def mean_note_user(self, id_user:int):

        query = """
        SELECT AVG(vote) AS vote_avg FROM projet_info.seenmovies
        WHERE id_user=%(id_user)s;
        """
        raw_note = self.db_connector.sql_query(query, {"id_user": id_user}, "one")
        return raw_note["vote_avg"] if raw_note else None
    
    def get_top_movies_liked_by_others_users(self, id_user:int, top:int=5):
        query = """
        SELECT M.*, COUNT(CASE WHEN SM.favorite=TRUE THEN 1 END) AS total_liked
        FROM projet_info.Movie M
        JOIN projet_info.SeenMovies SM ON M.id=SM.id_movie
        WHERE NOT EXISTS (
            SELECT 1
            FROM projet_info.SeenMovies SM2
            WHERE SM2.id_user = %(id_user)s
            AND SM2.id_movie = M.id
        )
        GROUP BY M.id
        HAVING COUNT(CASE WHEN SM.favorite = TRUE THEN 1 END) > 0
        ORDER BY total_liked DESC, vote_average DESC NULLS LAST LIMIT %(top)s;
        """
        raws_collection = self.db_connector.sql_query(query, {"id_user":id_user, "top":top}, "all" )
        
        return raws_collection

# Tests manuels
if __name__ == "__main__" :
    import dotenv
    dotenv.load_dotenv()
    db_connector = DBConnector()
    seen_movie_repo = SeenMovieRepo(db_connector)
    print(seen_movie_repo.get_new_follow_suggestions(5))

    