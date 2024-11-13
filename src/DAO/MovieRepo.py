from src.DAO.DBConnector import DBConnector
from src.Model.Movie import Movie

class  MovieRepo:
    db_connector : DBConnector

    def __init__(self, db_connector: DBConnector):

        self.db_connector = db_connector

    def insert_into_db(self, movies:list[dict]):
       
        query = """
        INSERT INTO projet_info.Movie (id, original_language, original_title, release_date, title, overview)
        VALUES %s
        """ 
        query += ", %s"*(len(movies)-1) +  "ON CONFLICT (id) DO NOTHING RETURNING id ;"
        
        # Préparer les valeurs pour l'insertion
        values = [
            (
                movie['id'], movie['original_language'], movie['original_title'],
                movie['release_date'], movie['title'], movie['overview']
            )
            for movie in movies
        ]

        raw_created = self.db_connector.sql_query(query, values, "none")
        
        return True if raw_created else False

    def update_vote(self, id_movie:int, vote_avg:float, vote_count:int):
        query = """
        UPDATE projet_info.Movie
        SET vote_average=%(vote_avg)s, vote_count=%(vote_count)s
        WHERE id=%(id_movie)s RETURNING *
        """
        raw_update = self.db_connector.sql_query(query, 
        {"id_movie":id_movie, "vote_avg":vote_avg, "vote_count":vote_count}, "one")
        
        return Movie(**raw_update) if raw_update else None

    
    def get_by_id(self, movie_id:int, user_id=None):
        query = """ 
        WITH myFollowers AS (
            SELECT id_follower 
            FROM projet_info.userfollowers UF 
            WHERE UF.id_user = %(user_id)s
        )
        SELECT 
            M.*, 
            (SELECT AVG(SM.vote)
            FROM projet_info.SeenMovies SM
            JOIN myFollowers mF ON SM.id_user = mF.id_follower
            WHERE SM.id_movie = M.id
            ) AS followers_average_vote
        FROM projet_info.Movie M
        WHERE M.id = %(movie_id)s;
        """
        raw_movie = self.db_connector.sql_query(query, {"movie_id":movie_id, "user_id": user_id}, "one")
        return raw_movie
        if raw_movie is None :
            return None
        else :
            return Movie(**raw_movie)

    def get_by_title(self, title:str, user_id=None):
        title = f"%{title}%"
        query = """ 
        WITH myFollowers AS (
            SELECT id_follower 
            FROM projet_info.userfollowers UF 
            WHERE UF.id_user = %(user_id)s
        )
        SELECT 
            M.*, 
            (SELECT AVG(SM.vote)
            FROM projet_info.SeenMovies SM
            JOIN myFollowers mF ON SM.id_user = mF.id_follower
            WHERE SM.id_movie = M.id
            ) AS follower_average_vote
        FROM projet_info.Movie M
        WHERE M.title LIKE %(title)s OR M.original_title LIKE %(title)s;
        """
        raws_movie = self.db_connector.sql_query(query, {"title": title, "user_id": user_id}, "all")
        return raws_movie
        if raws_movie is None :
            return []
        else :
            return [Movie(**raw_movie) for raw_movie in raws_movie]
    
    def get_by_release_period(self, start_release_date:str, end_release_date:str):
        raws_movie = self.db_connector.sql_query("SELECT * FROM Movie WHERE release_date BETWEEN %s AND %s;", (start_release_date, end_release_date), "all")
        if raws_movie is None :
            return []
        else :
            return [Movie(**raw_movie) for raw_movie in raws_movie]
    
    def get_lastest_released(self, number:int):
        raws_movie = self.db_connector.sql_query("SELECT * FROM Movie ORDER BY release_date DESC LIMIT %s;", (number,), return_type = "all")
        if raws_movie is None :
            return []
        else :
            return [Movie(**raw_movie) for raw_movie in raws_movie]
    
    def get_by_genre(self, name_genre:str):

        name_genre = f"%{name_genre}%"
        query = """SELECT * FROM projet_info.Genre G
        JOIN projet_info.MovieGenre MG ON G.id_genre = MG.id_genre
        LEFT projet_info.Movie M ON MG.id_movie = M.id
        WHERE G.name_genre LIKE %s;
        """
        raws_selected = self.db_connector.sql_query(query, [name_genre], "all")
        
        return [Movie(**raw_selected) for raw_selected in raws_selected] if raws_selected else []



if __name__ == "__main__" :
    import dotenv
    dotenv.load_dotenv()
    db_connector = DBConnector()
    movie_repo = MovieRepo(db_connector)
    print(movie_repo.get_by_title("a", 1))
    
    
   
