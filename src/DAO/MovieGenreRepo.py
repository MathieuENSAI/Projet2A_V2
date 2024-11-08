from typing import Optional
from src.DAO.DBConnector import DBConnector
from src.Model.MovieGenre import MovieGenre

class  MovieGenreRepo:
    db_connector : DBConnector

    def __init__(self, db_connector: DBConnector):

        self.db_connector = db_connector
    
    def insert_into_db(self,  movie_genres:list[dict]):
        query = """
        INSERT INTO  projet_info.MovieGenre (id_movie, id_genre)
        VALUES %s
        """ 
        query += ", %s"*(len(movie_genres)-1) +  " ON CONFLICT (id_movie, id_genre) DO NOTHING RETURNING id_movie id_genre;"
        # Préparer les valeurs pour l'insertion
        values = [(movie_genre['id_movie'], movie_genre['id_genre']) for movie_genre in movie_genres]
        raw_created = self.db_connector.sql_query(query, values, "none")

        return True if raw_created else False
    

   