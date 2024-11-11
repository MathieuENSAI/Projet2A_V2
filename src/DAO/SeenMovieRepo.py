from typing import Optional
from src.Model.SeenMovie import SeenMovie
from src.DAO.DBConnector import DBConnector
from src.Model.Movie import Movie
from src.Model.User import User


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

    def insert_into_db(self, id_user : int, id_movie : int, seen : bool=True, to_watch_later:bool=False,
                        watch_count:int=1, vote : int = None, favorite : bool = False) -> SeenMovie:
        raw_created_seenmovie = self.db_connector.sql_query(
                """INSERT INTO projet_info.seenmovies (id_user, id_movie, seen, to_watch_later, watch_count, vote, favorite)
                VALUES (%(id_user)s, %(id_movie)s, %(seen)s, %(to_watch_later)s, %(watch_count)s, %(vote)s, %(favorite)s)
                ON CONFLICT(id_user, id_movie) DO UPDATE
                SET watch_count = seenmovies.watch_count + 1,
                    seen = EXCLUDED.seen,
                    to_watch_later = EXCLUDED.to_watch_later,
                    vote = EXCLUDED.vote,
                    favorite = EXCLUDED.favorite
                RETURNING *;""",
                {"id_user": id_user, "id_movie": id_movie, "seen" : seen, "to_watch_later":to_watch_later, 
                "watch_count":watch_count, "vote" : vote, "favorite":favorite},"one")
        if raw_created_seenmovie is None:
            return None
        return SeenMovie(**raw_created_seenmovie)
    
    def update_db(self, seenmovie: SeenMovie):
        raw_update = self.db_connector.sql_query(
            """UPDATE projet_info.seenmovies
            SET seen = %(seen)s, 
                to_watch_later = %(to_watch_later)s,
                watch_count = %(watch_count)s,
                vote = %(vote)s,
                favorite = %(favorite)s
            WHERE id_user = %(id_user)s
            AND id_movie = %(id_movie)s;""",
            {
                "seen": seenmovie.seen,
                "to_watch_later" : seenmovie.to_watch_later,
                "watch_count" : seenmovie.watch_count,
                "vote": seenmovie.vote,
                "favorite": seenmovie.favorite,
                "id_user": seenmovie.id_user,
                "id_movie": seenmovie.id_movie
                },
                "none"
            )
        return True if raw_update else False

    
    def delete_from_db(self, seenmovie : SeenMovie):
        raw_delete = self.db_connector.sql_query(
            """DELETE FROM projet_info.seenmovies
               WHERE id_user = %(id_user)s
               AND  id_movie = %(id_movie)s""",
               {"id_user" : seenmovie.id_user,
                "id_movie" : seenmovie.id_movie}
        )
        return raw_delete.rowcount > 0
        
    def get_list_seenmovies_by_user(self, id_user : int) -> list[Movie]|None:
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
        list_movies = []

        if raw_movies:
            for movie in raw_movies:
                list_movies.append(Movie(**movie))
            return list_movies
        else : 
            return None
        
    def get_watchlist_user(self, id_user : int) -> list[Movie]|None:
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
        list_movies = []

        if raw_movies:
            for movie in raw_movies:
                list_movies.append(Movie(**movie))
            return list_movies
        else : 
            return None
        
    def get_list_favorite_movie(self, id_user : int) -> list[Movie]|None:
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
        list_movies = []

        if raw_movies:
            for row in raw_movies:
                list_movies.append(Movie(**row))
            return list_movies
        else : 
            return None
        
    def get_list_users_by_movie(self, id_movie : int) -> list[User]|None:
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
        list_users = []

        if raw_users:
            for user in raw_users:
                list_users.append(User(**user))
            return list_users
        else :
            return None
    
    def note_movie(self, id_user: int, id_movie: int, note: int):

        upsert_query = """
            INSERT INTO projet_info.seenmovies (id_user, id_movie, seen, watch_count, favorite, vote)
            VALUES (%(id_user)s, %(id_movie)s, TRUE, 1, FALSE, %(vote)s)
            ON CONFLICT (id_movie, id_user)
            DO UPDATE SET vote = EXCLUDED.vote;
        """
        self.db_connector.sql_query(upsert_query, {"id_user": id_user, "id_movie": id_movie, "vote": note}, "none")
        avg_query = """
            SELECT AVG(vote) AS vote_avg, COUNT(vote) AS vote_count 
            FROM projet_info.seenmovies
            WHERE id_movie = %(id_movie)s;
        """
        vote_movie = self.db_connector.sql_query(avg_query, {"id_movie": id_movie}, "one")
        
        return vote_movie if vote_movie else None

    def mean_note_user(self, id_user:int):

        query = """
        SELECT AVG(vote) AS vote_avg FROM projet_info.seenmovies
        WHERE id_user=%s AND  vote IS NOT NULL;
        """
        raw_note = self.db_connector.sql_query(query, [id_user], "one")
        return raw_note["vote_avg"] if raw_note else None



# Tests manuels
if __name__ == "__main__" :
    import dotenv
    dotenv.load_dotenv()
    db_connector = DBConnector()
    seen_movie_repo = SeenMovieRepo(db_connector)
    print(seen_movie_repo.note_movie(1, 200, 8))
    print(seen_movie_repo.mean_note_user(2))

    