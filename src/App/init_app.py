from dotenv import load_dotenv
load_dotenv()

from src.DAO.DBConnector import DBConnector
from src.DAO.UserRepo import UserRepo
from src.DAO.MovieRepo import MovieRepo
from src.DAO.GenreRepo import GenreRepo
from src.DAO.MovieGenreRepo import MovieGenreRepo
from src.Service.JWTService import JwtService
from src.Service.UserService import UserService
from src.Service.MovieService import MovieService
from src.Service.MovieFromTMDService import MovieFromTMDService
from src.Service.SchedulerService import SchedulerService


db_connector = DBConnector()
user_repo = UserRepo(db_connector)
movie_repo = MovieRepo(db_connector)
movie_genre_repo = MovieGenreRepo(db_connector)
genre_repo = GenreRepo(db_connector)
jwt_service = JwtService()
user_service = UserService(user_repo)
movie_TMDB = MovieFromTMDService()
movie_service = MovieService(movie_repo,movie_TMDB, movie_genre_repo)
scheduler_service = SchedulerService(movie_TMDB, genre_repo)
