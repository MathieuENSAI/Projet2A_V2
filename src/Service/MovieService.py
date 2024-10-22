from src.DAO.MovieRepo import MovieRepo
from src.Model.Movie import Movie

class MovieService:

    def __init__(self, movie_repo: MovieRepo):
        self.movie_rep = movie_repo
    
    def get_by_id(self, movie_id: str) -> Movie | None :
        return self.movie_rep.get_by_id(movie_id)
