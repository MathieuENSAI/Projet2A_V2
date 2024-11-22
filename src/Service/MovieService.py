from src.DAO.MovieRepo import MovieRepo
from src.DAO.MovieGenreRepo import MovieGenreRepo
from src.Service.MovieFromTMDService import MovieFromTMDService
from src.Model.Movie import Movie


class MovieService:

    def __init__(self, movie_repo: MovieRepo, movie_TMDB: MovieFromTMDService, movie_genre_repo:MovieGenreRepo):
        self.movie_repo = movie_repo
        self.movie_TMDB = movie_TMDB
        self.movie_genre_repo = movie_genre_repo
    
    def get_by_id(self, movie_id: int, user_id=None) -> Movie | None :
        movie = self.movie_repo.get_by_id(movie_id, user_id)
        if movie is not None:
            return movie

        movie = self.movie_TMDB.get_by_id(movie_id)
        if movie is not None:
            self.movie_repo.insert_into_db([movie['movie'].__dict__])
            self.movie_genre_repo.insert_into_db([movie['movie_genre']])
            movie = movie["movie"]
        return movie
    
    def get_by_title(self,title: str, user_id=None):
        movies = self.movie_repo.get_by_title(title, user_id)
        
        if len(movies)>=5:
            return movies
        elif movies is None:
            movies = []
        movie_not_in_db = []
        movies_from_TMDB = self.movie_TMDB.search_movie(title)
        for movie in movies_from_TMDB:
            movie = movie['movie']
            if movie.id not in [m.id for m in movies]:
                movie_not_in_db.append(movie)
    
        return movies + movie_not_in_db
    
    def get_by_genre(self,genre: str, user_id=None):
        movies = self.movie_repo.get_by_genre(genre, user_id)
        if len(movies)>=5:
            return movies
        elif movies is None:
            movies = []
        movie_not_in_db = []
        movies_from_TMDB = self.movie_TMDB.search_movie(genre)
        for movie in movies_from_TMDB:
            movie = movie['movie']
            if movie.id not in [m.id for m in movies]:
                movie_not_in_db.append(movie)
    
        return movies + movie_not_in_db
    


    def get_by_release_period(self, start_release_date: str, end_release_date: str):
        movies = self.movie_repo.get_by_release_period(start_release_date, end_release_date)
        if movies is None:
            movies = []
        movie_not_in_db = []
        movies_from_TMDB = self.movie_TMDB.get_by_release_period(start_release_date, end_release_date)
        for movie in movies_from_TMDB:
            movie = movie['movie']
            if movie.id not in (m.id for m in movies):
                movie_not_in_db.append(movie)
        return movies + movie_not_in_db

    def get_lastest_released(self, number:int)-> list[Movie]:
        movies = self.movie_TMDB.get_lastest_released(number)
        movies_genres = [movie['movie_genre'] for movie in movies]
        movies = [movie['movie'] for movie in movies]
        # Enrégistrer les 10 récents films en local
        self.movie_repo.insert_into_db([movie.__dict__ for movie in movies[:10]])
        self.movie_genre_repo.insert_into_db(movies_genres[:10])
        

        return movies

if __name__ == "__main__" :
    import dotenv
    from src.DAO.DBConnector import DBConnector
    dotenv.load_dotenv()
    db_connector = DBConnector()
    movie_repo = MovieRepo(db_connector)
    movie_genre_repo = MovieGenreRepo(db_connector)
    movie_TMDB = MovieFromTMDService()
    movie_service = MovieService(movie_repo, movie_TMDB, movie_genre_repo)
    print(movie_service.get_by_genre("comedi"))

    