from src.DAO.DBConnector import DBConnector
from src.Model.Genre import Genre

class  GenreRepo:
    db_connector : DBConnector

    def __init__(self, db_connector: DBConnector):

        self.db_connector = db_connector

    def insert_into_db(self, **genres):
        # Vérification de la présence de données
        if not genres:
            return None
        query = "INSERT INTO Movie(id_genre, id_name) VALUES (%s, %s)"
        if len(genres) > 1:
            query += ", (%s, %s)" * (len(genres) - 1)
        query += " RETURNING *;"

        data = tuple(attribut for genre in genres.values() for attribut in (genre['id'], genre['name']))

        raw_created = self.db_connector.sql_query(query, data, "all")

        if raw_created is None:
            return None
        else:
            return [Genre(**attributs) for attributs in raw_created]

  