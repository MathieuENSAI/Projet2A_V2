from src.Model.User import User 
from src.Model.Movie import Movie 
from src.DAO.SeenMovieRepo import SeenMovieRepo
from src.DAO.MovieRepo import MovieRepo

class NoteService :

    def __init__(self, movie_repo:MovieRepo, seen_movie_repo :SeenMovieRepo):
        self.movie_repo=movie_repo
        self.seen_movie_repo=seen_movie_repo
    
    def note_movie(self, id_user:int, id_movie:int, note:int):
        vote_movie = self.seen_movie_repo.note_movie(id_user, id_movie, note)
        if vote_movie:
            movie = self.movie_repo.update_vote(id_movie, vote_movie["vote_avg"], vote_movie["vote_count"])
            return movie
        return None
    
    def delete_note_movie(self, id_user:int, id_movie:int):
        if self.seen_movie_repo.delete_note_movie(id_user, id_movie):
            movie = self.movie_repo.update_vote(id_movie, vote_movie["vote_avg"], vote_movie["vote_count"])
            return movie
        return False
    
    