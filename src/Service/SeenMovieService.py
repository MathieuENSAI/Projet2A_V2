from src.Model.User import User
from src.Model.Movie import Movie
from src.DAO.UserRepo import UserRepo
from src.DAO.MovieRepo import MovieRepo
from src.Model.SeenMovie import SeenMovie
from src.DAO.SeenMovieRepo import SeenMovieRepo

class SeenMovieService:
    def seen_movie(self, user : User, movie : Movie)-> SeenMovie: 
        return SeenMovieRepo.insert_into_db(
            id_user=user.id_user,
            id_movie=movie.id,
            seen=True)
    
    def add_to_watchlist(self, user : User, movie : Movie)-> SeenMovie: 
        return SeenMovieRepo.insert_into_db(
            id_user=user.id_user,
            id_movie=movie.id,
            seen=False)
    
    def delete_seenmovie_by_id(self, id_seen_movie : int)-> bool:
        if SeenMovieRepo.get_by_id(id_seen_movie):
            seenmovie = SeenMovieRepo.get_by_id(id_seen_movie)
            return SeenMovieRepo.delete_from_db(seenmovie)
        else:
            print("Movie id not found in the database.")
    
    def delete_seenmovie_by_user_and_movie(self, user : User, movie : Movie)-> bool:
        if SeenMovieRepo.get_by_user_and_movie(user.id_user, movie.id):
            seenmovie = SeenMovieRepo.get_by_user_and_movie(user.id_user, movie.id)
            return SeenMovieRepo.delete_from_db(seenmovie)
        else:
            print("Not found in the database.")
    
    def watchlist(user : User):
        if SeenMovieRepo.get_watchlist_user(user.id_user):
            watchlist=[]
            list_movies = SeenMovieRepo.get_watchlist_user(user.id_user)
            for movie in list_movies:
                movie_to_watch = MovieRepo.get_by_id(movie)
                watchlist.append(movie_to_watch.title)
            return watchlist
        else:
            print("No movie found in this user's watchlist.")
    
    def seenmovies_user(user: User):
        if SeenMovieRepo.get_list_seenmovies_by_user(user.id_user):
            seenmovies=[]
            list_movies = SeenMovieRepo.get_watchlist_user(user.id_user)
            for movie in list_movies:
                watched_movie = MovieRepo.get_by_id(movie)
                seenmovies.append(watched_movie.title)
            return seenmovies
        else:
            print("No movie have been seen by this user.")
    
    def movies_seen_by(movie : Movie):
        if SeenMovieRepo.get_list_users_by_movie(movie.id):
            list_username=[]
            list_users = SeenMovieRepo.get_list_users_by_movie(movie.id)
            for user in list_users:
                username = UserRepo.get_by_id(user)
                list_username.append(username.username)
            return list_username
        else:
            print("This have not been seen by any user in our database.")

    def favorite_movie_user(user : User):
        if SeenMovieRepo.get_list_favorite_movie(user.id_user):
            list_favorite = []
            list_movies = SeenMovieRepo.get_list_favorite_movie(user.id_user)
            for movie in list_movies:
                favorite = MovieRepo.get_by_id(favorite)
                list_favorite.append(favorite.title)
            return list_favorite
        else:
            print("This user don't have favorite movies")