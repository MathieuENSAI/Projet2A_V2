from src.DAO.DBConnector import DBConnector
from src.Model.Genre import Genre

class  GenreRepo:
    db_connector : DBConnector

    def __init__(self, db_connector: DBConnector):

        self.db_connector = db_connector

    def insert_into_db(self, genres: list[Genre]):

        query = "INSERT INTO Genre(id_genre, name_genre) VALUES (%s, %s)"
        if len(genres)>1 :
            query += ", (%s, %s)"*(len(genres)-1)
        query += " RETURNING *;"
        data = tuple(attribut for genre in genres for attribut in (
            genre.id_genre, genre.name_genre
            ))

        raw_created = self.db_connector.sql_query(query, data, "all")
        if raw_created is None :
            return None
        else :
            return genres
  