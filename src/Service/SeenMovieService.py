from src.Model.User import User
from src.Model.Movie import Movie
from src.DAO.UserRepo import UserRepo
from src.DAO.MovieRepo import MovieRepo
from src.Model.SeenMovie import SeenMovie
from src.DAO.SeenMovieRepo import SeenMovieRepo

class SeenMovieService:

    def __init__(self, seenmovie_repo : SeenMovieRepo) -> None:
        self.seen_movierepo = seenmovie_repo

    def seen_movie(self, user : User, movie : Movie)-> SeenMovie: 
        return self.seen_movierepo.insert_into_db(
            id_user=user.id_user,
            id_movie=movie.id,
            seen=True)
    
    def add_to_watchlist(self, user : User, movie : Movie)-> SeenMovie: 
        return self.seen_movierepo.insert_into_db(
            id_user=user.id_user,
            id_movie=movie.id,
            seen=False)

    def delete_seenmovie_by_user_and_movie(self, user : User, movie : Movie)-> bool:
        if self.seen_movierepo.get_by_user_and_movie(user.id_user, movie.id):
            seenmovie = self.seen_movierepo.get_by_user_and_movie(user.id_user, movie.id)
            return self.seen_movierepo.delete_from_db(seenmovie)
        else:
            print("Not found in the database.")
    
    def watchlist(self, user : User):
        if self.seen_movierepo.get_watchlist_user(user.id_user):
            watchlist=[]
            list_movies = self.seen_movierepo.get_watchlist_user(user.id_user)
            for movie in list_movies:
                movie_to_watch = MovieRepo.get_by_id(movie)
                watchlist.append(movie_to_watch.title)
            return watchlist
        else:
            print("No movie found in this user's watchlist.")
    
    def seenmovies_user(self, user: User):
        if self.seen_movierepo.get_list_seenmovies_by_user(user.id_user):
            seenmovies=[]
            list_movies = self.seen_movierepo.get_watchlist_user(user.id_user)
            for movie in list_movies:
                watched_movie = MovieRepo.get_by_id(movie)
                seenmovies.append(watched_movie.title)
            return seenmovies
        else:
            print("No movie have been seen by this user.")
    
    def movies_seen_by(self, movie : Movie):
        if self.seen_movierepo.get_list_users_by_movie(movie.id):
            list_username=[]
            list_users = self.seen_movierepo.get_list_users_by_movie(movie.id)
            for user in list_users:
                username = UserRepo.get_by_id(user)
                list_username.append(username.username)
            return list_username
        else:
            print("This have not been seen by any user in our database.")

    def favorite_movie_user(self, user : User):
        if self.seen_movierepo.get_list_favorite_movie(user.id_user):
            list_favorite = []
            list_movies = self.seen_movierepo.get_list_favorite_movie(user.id_user)
            for movie in list_movies:
                favorite = MovieRepo.get_by_id(movie)
                list_favorite.append(favorite.title)
            return list_favorite
        else:
            print("This user don't have any favorite movie")