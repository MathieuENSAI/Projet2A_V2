from src.Model.SeenMovie import SeenMovie
from .DBConnector import DBConnector


class SeenMovieRepo:
    db_connector: DBConnector

    def __init__(self, db_connector: DBConnector):
        self.db_connector = db_connector

    def get_by_id(self, id_seenmovie: int) -> Optional[SeenMovie]:
        raw_seenmovie = self.db_connector.sql_query(
            """SELECT * from projet_info.seenmovies 
               WHERE id=%s""", [id_seenmovie], "one")
        if raw_seenmovie is None:
            return None
        return SeenMovie(**raw_seenmovie)
    
    def get_by_user_and_movie(self, id_user: int, id_movie: int ) -> Optional[SeenMovie]:
        raw_seenmovie = self.db_connector.sql_query(
            """SELECT * from projet_info.seenmovies 
               WHERE id_user =%(id_user)s
               AND id_movie =%(id_movie)s""",
               {"id_user":id_user, "id_movie":id_movie}, "one")
        if raw_seenmovie is None:
            return None
        return SeenMovie(**raw_seenmovie)

    def insert_into_db(self, id_user : int, id_movie : int, seen : bool, 
                        note : int = None, favorite : bool = False) -> SeenMovie:
        raw_created_seenmovie = self.db_connector.sql_query(
            """
        INSERT INTO seenmovies (id_seenmovie, id_user, id_movie, seen, note, favorite)
        VALUES (DEFAULT, %(id_user)s, %(id_movie)s, %(seen)s, %(note)s, %(favorite)s)
        RETURNING *;
        """,
            {"id_user": id_user, "id_movie": id_movie, "seen" : seen, "note" : note, 
             "favorite":favorite},
            "one",
        )

        return SeenMovie(**raw_created_seenmovie)
    
    def delete_from_db(self, seenmovie : SeenMovie):
        raw_delete = self.db_connector.sql_query(
            """DELETE FROM projet_info.seenmovies
               WHERE %(id_seenmovie)s = id_seenmovie""",
               {"id_seenmovie" : seenmovie.id_seenmovie}
        )
        return raw_delete.rowcount > 0
    
    def get_note(self, id_user : int, id_movie : int) -> SeenMovie: 
        raw_note = self.db_connector.sql_query(
            """
            SELECT note 
            FROM seenmovies 
            WHERE %(id_user)s = id_user 
            AND %(id_movie)s = id_movie)
            """,
            {"id_user": id_user, "id_movie": id_movie}, "one",
        )
        if raw_note : 
            return raw_note
        else :
            return("No note available.")
        
    def get_list_seenmovies_by_user(self, id_user : int) -> list[int]:
        """ Returns the list of movies id seen by a user"""
        raw_movies = self.db_connector.sql_query(
            """
            SELECT id_movie 
            FROM seenmovies 
            WHERE %(id_user)s = id_user
            AND seen = TRUE
            """,
            {"id_user": id_user}, "all",
        )
        list_movies = []

        if raw_movies:
            for row in raw_movies:
                list_movies.append(row["id_movie"])
            return list_movies
        else : 
            return ("No movie seen by this user.")
        
    def get_watchlist_user(self, id_user : int) -> list[int]:
        """ Returns the movies a user wanna see in the future"""
        raw_movies = self.db_connector.sql_query(
            """
            SELECT id_movie 
            FROM seenmovies 
            WHERE %(id_user)s = id_user
            AND seen = FALSE
            """,
            {"id_user": id_user}, "all",
        )
        list_movies = []

        if raw_movies:
            for row in raw_movies:
                list_movies.append(row["id_movie"])
            return list_movies
        else : 
            return ("No movie in this user's watchlist.")
        
    def get_list_favorite_movie(self, id_user : int) -> list[int]:
        """ Returns the list of favorite movies of an user"""
        raw_movies = self.db_connector.sql_query(
            """
            SELECT id_movie 
            FROM seenmovies 
            WHERE %(id_user)s = id_user
            AND favorite = TRUE
            """,
            {"id_user": id_user}, "all",
        )
        list_movies = []

        if raw_movies:
            for row in raw_movies:
                list_movies.append(row["id_movie"])
            return list_movies
        else : 
            return ("This user don't have any favorite movie")
        
    def get_list_users_by_movie(self, id_movie : int) -> list[int]:
        """ Returns the list of users who have seen a movie"""
        raw_users = self.db_connector.sql_query(
            """
            SELECT id_user 
            FROM seenmovies 
            WHERE %(id_movie)s = id_movie
            AND seen = TRUE
            """,
            {"id_movie": id_movie}, "all",
        )
        list_users = []

        if raw_users:
            for row in raw_users:
                list_users.append(row["id_users"])
            return list_users
        else : 
            return ("This movie hasn't been seen by any user.")
        