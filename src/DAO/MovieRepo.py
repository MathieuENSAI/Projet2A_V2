from typing import Optional

from src.DAO.DBConnector import DBConnector
from src.Model.Movie import Movie

class  MovieRepo:
    db_connector : DBConnector

    def __init__(self, db_connector: DBConnector):

        self.db_connector = db_connector
    
    def get_by_id(self, movie_id:int):

        raw_movie = self.db_connector.sql_query("SELECT * FROM Movie WHERE movie_id = %s", (movie_id), "one")

        if raw_movie is None :
            return None
        else :
            return Movie(**raw_movie)


