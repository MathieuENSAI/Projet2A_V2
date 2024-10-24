from typing import Optional

from src.DAO.UserRepo import UserRepo
from src.Model.User import User
from src.Service.PasswordService import check_password_strength, create_salt, hash_password, validate_username_password


class UserService:
    def __init__(self, user_repo: UserRepo):
        self.user_repo = user_repo

    def create_user(self, username: str, password: str) -> User:
        salt = create_salt()
        pass_word = hash_password(password, salt)
        user = self.user_repo.insert_into_db(username = username, salt = salt, hashed_password=pass_word)
        return(user)

    def get_user_by_id(self, user_id: int) -> User | None:
        return self.user_repo.get_by_id(user_id)
    
    def login_user(self, username: str, password: str) -> Optional[User]:
        #user = self.user_repo.get_by_username(username)
        #if user is None:
        #    return None
        #hashed_password = hash_password(password, user.salt)
        #if hashed_password == user.hashed_password:
        #    return user
        #return None
        self.user_repo.login(username=username, password=password)

    def delete_user(self, user_id: int) -> None:
        user = self.get_user_by_id(user_id)
        if user is None:
            raise ValueError("User not found")
        self.user_repo.delete_from_db(user)

    def check_username(self, username: str) -> bool:
        if self.user_repo.get_by_username(username=username) == None:
            return False
        return True
    
    def search_user(self, username: str) -> User:
        user = self.user_repo.get_by_username(username=username)
        if user == None:
            raise Exception("This User didn't exist.")
        return user
    
    
    # def disconnection():
    #     ##TODO
from typing import Optional

from src.DAO.UserRepo import UserRepo
from src.Model.User import User
from src.Service.PasswordService import check_password_strength, create_salt, hash_password, validate_username_password


class UserService:
    def __init__(self, user_repo: UserRepo):
        self.user_repo = user_repo

    def create_user(self, username: str, password: str) -> User:
        salt = create_salt()
        pass_word = hash_password(password, salt)
        user = self.user_repo.insert_into_db(username = username, salt = salt, hashed_password=pass_word)
        return(user)

    def get_user_by_id(self, user_id: int) -> User | None:
        return self.user_repo.get_by_id(user_id)
    
    def login_user(self, username: str, password: str) -> Optional[User]:
        #user = self.user_repo.get_by_username(username)
        #if user is None:
        #    return None
        #hashed_password = hash_password(password, user.salt)
        #if hashed_password == user.hashed_password:
        #    return user
        #return None
        self.user_repo.login(username=username, password=password)

    def delete_user(self, user_id: int) -> None:
        user = self.get_user_by_id(user_id)
        if user is None:
            raise ValueError("User not found")
        self.user_repo.delete_from_db(user)

    def check_username(self, username: str) -> bool:
        if self.user_repo.get_by_username(username=username) == None:
            return False
        return True
    
    def search_user(self, username: str) -> User:
        user = self.user_repo.get_by_username(username=username)
        if user == None:
            raise Exception("This User didn't exist.")
        return user
    
    
    #def disconnection():
        ##TODO