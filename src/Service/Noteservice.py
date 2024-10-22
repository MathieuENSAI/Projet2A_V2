from src.Model.User import User 
from src.Model.Movie import Movie 
from src.DAO.SeenMovieRepo import SeenMovieRepo

class NoteService :

    def get_note(self, user : User, movie : Movie):
        seenmovie = SeenMovieRepo.get_by_user_and_movie(user.id_user, movie.id)
        if seenmovie is not None : 
            return seenmovie.note
        else : 
            return None
    
    def mean_note_user(self, user : User):
        list_movies = SeenMovieRepo.get_list_seenmovies_by_user(user.id_user)
        if list_movies is not None : 
            sum = 0
            len = 0
            for movie in len(list_movies):
                if NoteService.get_note(user.id_user,list_movies[movie]):
                    note = NoteService.get_note(user.id_user,list_movies[movie])
                    sum += note
                    len += 1
            return sum/len
        else :
            return None