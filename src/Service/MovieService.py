from src.DAO.MovieRepo import MovieRepo
from src.Service.MovieFromTMDService import MovieFromTMDService
from src.Model.Movie import Movie


class MovieService:

    def __init__(self, movie_repo: MovieRepo, movie_TMDB: MovieFromTMDService):
        self.movie_repo = movie_repo
        self.movie_TMDB = movie_TMDB
    
    def get_by_id(self, movie_id: int) -> Movie:
        movie = self.movie_repo.get_by_id(movie_id)
        if movie is not None:
            return movie

        movie = self.movie_TMDB.get_by_id(movie_id)
        if movie is not None:
            movie_repo.insert_into_db(movie)
            return movie
        
        raise FileNotFoundError()

    def get_by_title(self,title: str):
        movies = self.movie_repo.get_by_title(title)
        if movies is None:
            movies = []
        movies_from_TMDB = self.movie_TMDB.get_by_title(title)
        for movie in movies_from_TMDB:
            if movie.id not in (m.id for m in movies):
                unique_movies.append(movie)
        return movies

    def get_by_release_date(self, release_date: str):
        movies = self.movie_repo.get_by_release_date(release_date)
        if movies is None:
            movies = []
        movies_from_TMDB = self.movie_TMDB.get_by_release_date(release_date)
        for movie in movies_from_TMDB:
            if movie.id not in (m.id for m in movies):
                unique_movies.append(movie)
        return movies