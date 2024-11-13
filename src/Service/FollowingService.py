from src.DAO.FollowingRepo import FollowingRepo
from src.DAO.UserRepo import UserRepo
from src.Model.User import User


class FollowingService:
    def __init__(self, following_repo : FollowingRepo, user_repo : UserRepo):
        self.following_repo = following_repo
        self.user_repo = user_repo

    def get_all_following(self, user_id : int) -> list[User] :
       
        user_following = self.following_repo.get_all_following(user_id)
    
    def add_scout(self, user: User, scout: User) -> User:
        self.following_repo.add_scout(user, scout)

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

   