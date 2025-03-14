from src.Model.User import User
from src.Model.Movie import Movie
from src.DAO.UserRepo import UserRepo
from src.DAO.MovieRepo import MovieRepo
from src.Model.SeenMovie import SeenMovie
from src.DAO.SeenMovieRepo import SeenMovieRepo

class SeenMovieService:

    def __init__(self, seenmovie_repo : SeenMovieRepo) -> None:
        self.seen_movierepo = seenmovie_repo

    def watch_movie(self, id_user : int, id_movie : int)-> SeenMovie: 
        return self.seen_movierepo.insert_into_db(
            id_user=id_user,
            id_movie=id_movie,
            seen=True)

    def add_to_watchlist(self, id_user : int, id_movie : int)-> SeenMovie:
        seenmovie = self.seen_movierepo.get_by_user_and_movie(id_user, id_movie)
        if seenmovie is None:
            return self.seen_movierepo.insert_into_db(
                id_user=id_user,
                id_movie=id_movie,
                seen=False,
                to_watch_later=True)
        elif not seenmovie.to_watch_later:
            seenmovie.to_watch_later = True
            return self.seen_movierepo.update_db(seenmovie)
        return True
    
    def remote_from_user_watchlists(self, id_user:int, id_movie:int):
        return self.seen_movierepo.remove_from_user_watchlist(id_user, id_movie)

    def add_to_favoritelist(self, id_user:int, id_movie:int) -> SeenMovie:
        seenmovie = self.seen_movierepo.get_by_user_and_movie(id_user, id_movie)
        if seenmovie is None:
            return self.seen_movierepo.insert_into_db(
                id_user=id_user,
                id_movie=id_movie,
                seen=True,
                favorite=True)
        elif not seenmovie.favorite:
            seenmovie.favorite = True
            return self.seen_movierepo.update_db(seenmovie)
        return True
    
    def remote_from_user_favorites(self, id_user:int, id_movie:int):
        return self.seen_movierepo.remove_from_user_favorites(id_user, id_movie)
    
    def user_watchlist(self, id_user : int) -> list[Movie]:
        list_movies = self.seen_movierepo.get_watchlist_movie(id_user)
        if list_movies:
            return list_movies
        else:
            return None
    
    def user_seenmovies(self, id_user: int)-> list[Movie]:
        list_movies = self.seen_movierepo.get_movies_seen_by_user(id_user)
        if list_movies :
            return list_movies
        else:
            return None

    def user_favorites_movie(self, id_user : int) -> list[User]:
        list_movies = self.seen_movierepo.get_user_favorites_movie(id_user)
        if list_movies:
            return list_movies
        else:
            return None
    
    def get_top_movies_liked_by_others_users(self, id_user:int, top:int=5):
        return self.seen_movierepo.get_top_movies_liked_by_others_users(id_user, top)

    def mean_note(self, id_user:int):
        return self.seen_movierepo.mean_note_user(id_user)