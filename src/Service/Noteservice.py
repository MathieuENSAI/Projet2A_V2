from src.Model.User import User 
from src.Model.Movie import Movie 
from src.DAO.SeenMovieRepo import SeenMovieRepo

class NoteService :

    def __init__(self, seen_movie_repo :SeenMovieRepo):
        self.seen_movie_repo=seen_movie_repo

    def get_note(self, id_user : int, id_movie : int):
        seenmovie = self.seen_movie_repo.get_by_user_and_movie(id_user, id_movie)
        if seenmovie is not None : 
            return seenmovie.note
        else : 
            return None
    
    def mean_note_user(self, id_user : int):
        list_movies = self.seen_movie_repo.get_list_seenmovies_by_user(user.id_user)
        if list_movies is not None : 
            sum = 0
            len = 0
            for id_movie in list_movies:
                note = self.get_note(id_user, id_movie)
                if note:
                    sum += note
                    len += 1
            return sum/len
        else :
            return None