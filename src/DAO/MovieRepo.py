from typing import Optional
from datetime import date
from src.DAO.DBConnector import DBConnector
from src.Model.Movie import Movie

class  MovieRepo:
    db_connector : DBConnector

    def __init__(self, db_connector: DBConnector):

        self.db_connector = db_connector

    def insert_into_db(self, movies: list[Movie]):

        query = "INSERT INTO Movie(id, original_language, original_title, release_date, title, overview) VALUES (%s, %s, %s, %s, %s, %s)"
        if len(movies)>1 :
            query += ", (%s, %s, %s, %s, %s, %s)"*(len(movies)-1)
        query += " RETURNING *;"
        data = tuple(atribut for movie in movies for attribut in (
            movie.id, movie.original_language, movie.original_title, movie.release_date, movie.title, movie.overview
            ))

        raw_created = self.db_connector.sql_query(query, data, "all")
        if raw_movie is None :
            return None
        else :
            return movies
    
    def get_by_id(self, movie_id:int):
        raw_movie = self.db_connector.sql_query("SELECT * FROM Movie WHERE id = %s;", (movie_id), "one")
        if raw_movie is None :
            return None
        else :
            return Movie(**raw_movie)

    def get_by_title(self, title:str):
        raws_movie = self.db_connector.sql_query("SELECT * FROM Movie WHERE title = %s OR original_title = %s;", (title, title), "all")
        if raws_movie is None :
            return None
        else :
            return [Movie(**raw_movie) for raw_movie in raws_movie]
    
    def get_by_release_date(self, release_date:date):
        raws_movie = self.db_connector.sql_query("SELECT * FROM Movie WHERE release_date = %s;", (release_date), "all")
        if raws_movie is None :
            return None
        else :
            return [Movie(**raw_movie) for raw_movie in raws_movie]
    
    def get_lastest_released(self, number:int):
        raws_movie = self.db_connector.sql_query("SELECT * FROM Movie ORDER BY release_date DESC LIMIT %s;", (number), return_type = "all")
        if raws_movie is None :
            return None
        else :
            return [Movie(**raw_movie) for raw_movie in raws_movie]



