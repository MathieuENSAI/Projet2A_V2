from typing import Optional
from datetime import date
from src.DAO.DBConnector import DBConnector
from src.Model.Movie import Movie

class  MovieRepo:
    db_connector : DBConnector

    def __init__(self, db_connector: DBConnector):

        self.db_connector = db_connector

    def insert_into_db(self, movies:list[dict]):
        query = "INSERT INTO Movie(id, original_language, original_title, release_date, title, overview) VALUES (%s, %s, %s, %s, %s, %s)"
        if len(movies) > 1:
            query += ", (%s, %s, %s, %s, %s, %s)" * (len(movies) - 1)
        query += " RETURNING *;"

        data = tuple(attribut for movie in movies for attribut in (
            movie['id'], movie['original_language'], movie['original_title'], movie['release_date'], movie['title'], movie['overview']
        ))

        raw_created = self.db_connector.sql_query(query, data, "all")

        if raw_created is None:
            return None
        else:
            return [Movie(**attributs) for attributs in raw_created]
    
    def get_by_id(self, movie_id:int):
        raw_movie = self.db_connector.sql_query("SELECT * FROM Movie WHERE id = %(movie_id)s;", {"movie_id":movie_id}, "one")
        if raw_movie is None :
            return None
        else :
            return Movie(**raw_movie)

    def get_by_title(self, title:str):
        title = f"%{title}%"
        raws_movie = self.db_connector.sql_query("SELECT * FROM Movie WHERE (title LIKE %s ) OR (original_title LIKE %s);", (title, title), "all")
        if raws_movie is None :
            return None
        else :
            return [Movie(**raw_movie) for raw_movie in raws_movie]
    
    def get_by_release_period(self, start_release_date:str, end_release_date:str):
        raws_movie = self.db_connector.sql_query("SELECT * FROM Movie WHERE release_date BETWEEN %s AND %s;", (start_release_date, end_release_date), "all")
        if raws_movie is None :
            return None
        else :
            return [Movie(**raw_movie) for raw_movie in raws_movie]
    
    def get_lastest_released(self, number:int):
        raws_movie = self.db_connector.sql_query("SELECT * FROM Movie ORDER BY release_date DESC LIMIT %s;", (number,), return_type = "all")
        if raws_movie is None :
            return None
        else :
            return [Movie(**raw_movie) for raw_movie in raws_movie]



if __name__ == "__main__" :
    import dotenv
    dotenv.load_dotenv()
    db_connector = DBConnector()
    movie_repo = MovieRepo(db_connector)
    
   
