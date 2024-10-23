from typing import Optional
from src.DAO.DBConnector import DBConnector
from src.Model.MovieGenre import MovieGenre

class  MovieGenreRepo:
    db_connector : DBConnector

    def __init__(self, db_connector: DBConnector):

        self.db_connector = db_connector

    def insert_into_db(self, **movieGenres):
        # Vérification de la présence de données
        if not movieGenres:
            return None
        query= "INSERT INTO MovieGenres(id_movie, id_genre) VALUES (%s, %s)"
        if len(movieGenres) > 1:
            query += ", (%s, %s)" * (len(movieGenres) - 1)
        query += " RETURNING *;"

        data = tuple(attribut for movieGenres in movieGenress.values() for attribut in (
            movieGenre['id_movie'], movieGenre["id_genre"]
        ))

        raw_created = self.db_connector.sql_query(query, data, "all")

        if raw_created is None:
            return None
        else:
            return [MovieGenre(**attributs) for attributs in raw_created]