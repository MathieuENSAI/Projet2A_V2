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
        if self.seen_movierepo.get_watchlist_user(id_user):
            list_movies = self.seen_movierepo.get_watchlist_user(id_user)*
            print("The list of movies in this user's watchlist.")
            for movie in list_movies:
                movie.info()
        else:
            print("No movie found in this user's watchlist.")
    
    def seenmovies_user(self, id_user: int):
        if self.seen_movierepo.get_list_seenmovies_by_user(id_user):
            list_movies = self.seen_movierepo.get_watchlist_user(id_user)
            print("The list of movies watched by this user.")
            for movie in list_movies:
                movie.info()
        else:
            print("No movie have been seen by this user.")
    
    def movies_seen_by(self, id_movie : int):
        if self.seen_movierepo.get_list_users_by_movie(id_movie):
            list_users = self.seen_movierepo.get_list_users_by_movie(id_movie)
            print("This movie have been seen by those users:")
            for user in list_users:
                print(user.username)
        else:
            print("This have not been seen by any user in our database.")

    def favorite_movie_user(self, id_user : int):
        if self.seen_movierepo.get_list_favorite_movie(id_user):
            list_movies = self.seen_movierepo.get_list_favorite_movie(id_user)
            print("The list of favorite movies of this user:")
            for movie in list_movies:
                movie.info()
        else:
            print("This user don't have any favorite movie")