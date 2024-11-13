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
        
    def get_following_seen_movies(self, id_following:int):
        return self.following_repo.get_following_seen_movies(id_following)
    
    def get_movies_seen_together(self, id_user:int, id_following:int):
        return self.following_repo.get_movies_seen_together(id_user, id_following)

    def get_following_movies_collection(self, id_user:int, id_following:int):
        return {"following_seen_movies": self.get_following_seen_movies(id_following),
        "movies_seen_together": self.get_movies_seen_together(id_user, id_following)}
    
    def get_all_following(self, user_id : int) -> list[User] :
       
        user_following = self.following_repo.get_all_following(user_id)

    def remove_scout(self, user: User, scout: User) -> User:
        self.following_repo.remove_scout(user, scout)

    #def get_following_list(self, user_id) -> list[User] :
            #user = self.user_repo.get_by_id(user_id)
            #following = user.following
            #list_of_following = []
            #for id in following:
                #list_of_following.append(self.get_user_by_id(id))
            #return list_of_following
                

    #def add_following(self, me_id : int, user_to_add : int) -> list[User] :
        #following = self.get_following_list(me_id)
        #user = self.get_user_by_id(user_to_add)
        #if user in following:
            #raise Exception("You allready follow this user.")
        #else :
            #following.append(user)
        #return following
        
    #def delete_following(self, me_id: int, user_to_delete : int) -> list[User] :
        #following = self.get_following_list(me_id)
        #user = self.get_user_by_id(user_to_delete)
        #if not user in following:
            #raise Exception("You allready didn't follow this user.")
        #else :
            #following.remove(user)
        #return following

   