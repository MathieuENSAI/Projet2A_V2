from src.DAO.DBConnector import DBConnector
from src.Model.Genre import Genre

class  GenreRepo:
    db_connector : DBConnector

    def __init__(self, db_connector: DBConnector):

        self.db_connector = db_connector

    def insert_into_db(self, genres:list[dict]):
        query = """
        INSERT INTO Genre (id_genre, name_genre)
        VALUES %s
        """ 
        query += ", %s"*(len(genres)-1) +  " ON CONFLICT (id_genre) DO NOTHING RETURNING id_genre;"
        # Préparer les valeurs pour l'insertion
        values = [(genre['id_genre'], genre['name_genre']) for genre in genres]
        raw_created = self.db_connector.sql_query(query, values, "all")

        return True if raw_created else False

  