from typing import Optional

from DBConnector import DBConnector
from src.Model.Movie import Movie

class  MovieRepo:
    db_connector : DBConnector

    def __init__(self, db_connector: DBConnector):

        self.db_connector = db_connector
    
    def get_by_id(self, id_movie:int):

        res = self.db_connector.sql_query("SELECT * FROM Movie WHERE id_movie = %s", (id_movie), "one")
        
