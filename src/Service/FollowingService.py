from src.DAO.FollowingRepo import FollowingRepo
from src.DAO.UserRepo import UserRepo
from src.Model.User import User
from src.DAO.MovieRepo import MovieRepo

class FollowingService:
    def __init__(self, following_repo : FollowingRepo):
        self.following_repo = following_repo
        #self.user_repo = user_repo
        #self.movie_repo = movie_repo

    def add_following(self, id_user: int, id_following: int) :
        return self.following_repo.add_following(id_user, id_following)
    
    def stop_follow(self, id_user:int, id_following:int):
        return self.following_repo.delete_following(id_user, id_following)
    
    def is_user_follow(self, id_user:int, id_following:int):
        return self.following_repo.is_user_follow(id_user, id_following)
    
    def get_all_following(self, user_id : int) -> list[User] :
        return self.following_repo.get_all_following(user_id)

    def get_following_movies_collection(self, id_user:int, id_following:int):
        return {"following_seen_movies": self.following_repo.get_following_seen_movies(id_following),
        "movies_seen_together": self.following_repo.get_movies_seen_together(id_user, id_following)}