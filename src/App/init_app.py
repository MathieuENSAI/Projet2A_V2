from dotenv import load_dotenv

from src.DAO.DBConnector import DBConnector
from src.DAO.UserRepo import UserRepo
from src.DAO.MovieRepo import MovieRepo
from src.Service.JWTService import JwtService
from src.Service.UserService import UserService
from src.Service.MovieService import MovieService

load_dotenv()
db_connector = DBConnector()
user_repo = UserRepo(db_connector)
jwt_service = JwtService()
user_service = UserService(user_repo)
movie_repo = MovieRepo(db_connector)
movie_service = MovieService(movie_repo)
