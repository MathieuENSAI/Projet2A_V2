from dotenv import load_dotenv
load_dotenv()

from src.DAO.DBConnector import DBConnector
from src.DAO.UserRepo import UserRepo
from src.DAO.FollowingRepo import FollowingRepo
from src.DAO.MovieRepo import MovieRepo
from src.DAO.SeenMovieRepo import SeenMovieRepo
from src.DAO.GenreRepo import GenreRepo
from src.DAO.MovieGenreRepo import MovieGenreRepo
from src.Service.JWTService import JwtService
import src.Service.PasswordService as PasswordService
from src.Service.UserService import UserService
from src.Service.FollowingService import FollowingService
from src.Service.MovieService import MovieService
from src.Service.Noteservice import NoteService
from src.Service.MovieFromTMDService import MovieFromTMDService
from src.Service.SeenMovieService import SeenMovieService
from src.Service.SchedulerService import SchedulerService


db_connector = DBConnector()
user_repo = UserRepo(db_connector)
following_repo = FollowingRepo(db_connector)
movie_repo = MovieRepo(db_connector)
seen_movie_repo = SeenMovieRepo(db_connector)
movie_genre_repo = MovieGenreRepo(db_connector)
genre_repo = GenreRepo(db_connector)
jwt_service = JwtService()
user_service = UserService(user_repo, PasswordService)
following_service = FollowingService(following_repo)
movie_TMDB = MovieFromTMDService()
movie_service = MovieService(movie_repo, movie_TMDB, movie_genre_repo)
seen_movie_service = SeenMovieService(seen_movie_repo)
note_service = NoteService(movie_repo, seen_movie_repo)
scheduler_service = SchedulerService(movie_TMDB, genre_repo)
