from typing import Optional
from src.DAO.DBConnector import DBConnector
from src.Model.MovieGenre import MovieGenre

class  MovieGenreRepo:
    db_connector : DBConnector

    def __init__(self, db_connector: DBConnector):

        self.db_connector = db_connector
    
    def insert_into_db(self,  movie_genres:list[dict]):
        
        # Préparer les valeurs pour l'insertion
        data=[]
        for movie_genre in movie_genres:
            for genre in movie_genre['genres'] :
                if type(genre) is int:
                    data.append((movie_genre['id_movie'], genre))

                elif  type(genre) is dict and type(genre.get('id', None)) is int:
                    data.append((movie_genre['id_movie'], genre['id']))
        
        query = """
        INSERT INTO  projet_info.MovieGenre (id_movie, id_genre)
        VALUES %s
        """ 
        query += ", %s"*(len(data)-1) +  " ON CONFLICT (id_movie, id_genre) DO NOTHING RETURNING id_movie id_genre;"

        raw_created = self.db_connector.sql_query(query, data, "all")

        return True if raw_created else False

if __name__ == "__main__" :
    import dotenv
    dotenv.load_dotenv()
    db_connector = DBConnector()
    movie_genre_repo = MovieGenreRepo(db_connector)
    data = [ {'id_movie': 500, 'genres': [2]},
    {'id_movie': 505, 'genres': [{'id': 2, 'name': 'action'}, {'id': 3, 'name': 'comedi'}]}
    ]
    print(movie_genre_repo.insert_into_db(data))
    
    

   