from typing import Optional
from src.Model.SeenMovie import SeenMovie
from .DBConnector import DBConnector


class SeenMovieRepo:
    db_connector: DBConnector

    def __init__(self, db_connector: DBConnector):
        self.db_connector = db_connector

    # def get_by_id(self, id_seenmovie: int) -> Optional[SeenMovie]:
    #     raw_seenmovie = self.db_connector.sql_query(
    #         """SELECT * from projet_info.seenmovies 
    #            WHERE id_seenmovie=%s""", [id_seenmovie], "one")
    #     if raw_seenmovie is None:
    #         return None
    #     return SeenMovie(**raw_seenmovie)
    
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
                        vote : int = None, favorite : bool = False) -> SeenMovie:
        raw_created_seenmovie = self.db_connector.sql_query(
            """
        INSERT INTO projet_info.seenmovies (id_user, id_movie, seen, vote, favorite)
        VALUES (%(id_user)s, %(id_movie)s, %(seen)s, %(vote)s, %(favorite)s)
        RETURNING *;
        """,
            {"id_user": id_user, "id_movie": id_movie, "seen" : seen, "vote" : vote, 
             "favorite":favorite},
            "one",
        )

        return SeenMovie(**raw_created_seenmovie)
    
    def update_db(self, seenmovie : SeenMovie):
        raw_update = self.db_connector.sql_query (
        """UPDATE projet_info.seenmovies                            "
           SET seen      = %(seen)s, 
           vote   = %(vote)s,
           favorite = %(favorite)s, 
           WHERE id_user = %(id_user)s
           AND id_movie = %(id_movie)s;    """,
                        { "seen" :seenmovie.seen, 
                         "vote" :seenmovie.vote,
                         "favorite" : seenmovie.favorite,
                         "id_user" : seenmovie.id_user,
                         "id_movie":seenmovie.id_movie
                        }
                    )
        return raw_update ==1
    
    def delete_from_db(self, seenmovie : SeenMovie):
        raw_delete = self.db_connector.sql_query(
            """DELETE FROM projet_info.seenmovies
               WHERE id_user = %(id_user)s
               AND  id_movie = %(id_movie)s""",
               {"id_user" : seenmovie.id_user,
                "id_movie" : seenmovie.id_movie}
        )
        return raw_delete.rowcount > 0
    
    # def get_vote(self, id_user : int, id_movie : int) -> SeenMovie: 
    #     raw_vote = self.db_connector.sql_query(
    #         """
    #         SELECT vote 
    #         FROM seenmovies 
    #         WHERE %(id_user)s = id_user 
    #         AND %(id_movie)s = id_movie)
    #         """,
    #         {"id_user": id_user, "id_movie": id_movie}, "one",
    #     )
    #     if raw_vote : 
    #         return raw_vote
    #     else :
    #         return("No vote available.")
        
    def get_list_seenmovies_by_user(self, id_user : int) -> list[int]:
        """ Returns the list of movies id seen by a user"""
        raw_movies = self.db_connector.sql_query(
            """
            SELECT id_movie 
            FROM projet_info.seenmovies 
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
            return None
        
    def get_watchlist_user(self, id_user : int) -> list[int]:
        """ Returns the movies a user wanna see in the future"""
        raw_movies = self.db_connector.sql_query(
            """
            SELECT id_movie 
            FROM projet_info.seenmovies 
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
            return None
        
    def get_list_favorite_movie(self, id_user : int) -> list[int]:
        """ Returns the list of favorite movies of an user"""
        raw_movies = self.db_connector.sql_query(
            """
            SELECT id_movie 
            FROM projet_info.seenmovies 
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
            return None
        
    def get_list_users_by_movie(self, id_movie : int) -> list[int]:
        """ Returns the list of users who have seen a movie"""
        raw_users = self.db_connector.sql_query(
            """
            SELECT id_user 
            FROM projet_info.seenmovies 
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
            return None