from src.Model.User import User
from src.Model.Movie import Movie
from src.DAO.UserRepo import UserRepo
from src.DAO.MovieRepo import MovieRepo
from src.Model.SeenMovie import SeenMovie
from src.DAO.SeenMovieRepo import SeenMovieRepo

class SeenMovieService:

    def __init__(self, seenmovie_repo : SeenMovieRepo) -> None:
        self.seen_movierepo = seenmovie_repo

    def seen_movie(self, id_user : int, id_movie : int)-> SeenMovie: 
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

    
    def delete_seenmovie_by_user_and_movie(self, id_user : int, id_movie : int)-> bool:
        if self.seen_movierepo.get_by_user_and_movie(id_user, id_movie):
            seenmovie = self.seen_movierepo.get_by_user_and_movie(id_user, id_movie)
            return self.seen_movierepo.delete_from_db(seenmovie)
        else:
            print("Not found in the database.")
    
    def watchlist(self, id_user : int):
        list_movies = self.seen_movierepo.get_watchlist_user(id_user)
        if list_movies:
            for movie in list_movies:
                return movie
        else:
            return None
    
    def seenmovies_user(self, id_user: int):
        list_movies = self.seen_movierepo.get_watchlist_user(id_user)
        if list_movies :
            for movie in list_movies:
                return movie
        else:
            return None
    
    def movies_seen_by(self, id_movie : int):
        list_users = self.seen_movierepo.get_list_users_by_movie(id_movie)
        if list_users:
            for user in list_users:
                return user
        else:
            return None

    def favorite_movie_user(self, id_user : int):
        list_movies = self.seen_movierepo.get_list_favorite_movie(id_user)
        if list_movies:
            for movie in list_movies:
                return movie
        else:
            return None