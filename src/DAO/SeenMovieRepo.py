from src.Model.SeenMovie import SeenMovie

from .DBConnector import DBConnector


class SeenMovieRepo:
    db_connector: DBConnector

    def __init__(self, db_connector: DBConnector):
        self.db_connector = db_connector

    def get_by_id(self, id_seenmovie: int) -> Optional[SeenMovie]:
        raw_seenmovie = self.db_connector.sql_query("SELECT * from seenmovies WHERE id=%s", [id_seenmovie], "one")
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
        
    def get_list_seenmovies(self, id_user : int) -> list[SeenMovie]:
        """ Returns the list of movies id seen by a user"""
        raw_movies = self.db_connector.sql_query(
            """
            SELECT * 
            FROM seenmovies 
            WHERE %(id_user)s = id_user
            AND seen = TRUE
            """,
            {"id_user": id_user}, "all",
        )
        list_movies = []

        if raw_movies:
            for row in raw_movies:
                utilisateur = Utilisateur(
                    id_utilisateur=row["id_utilisateur"],
                    pseudo=row["pseudo"],
                    mdp=row["mdp"]
                )

                liste_utilisateurs.append(utilisateur)

        return liste_utilisateurs
