from typing import Optional

from src.DAO.UserRepo import UserRepo
from src.Model.User import User
import src.Service.PasswordService as PasswordService

class UserService:
    def __init__(self, user_repo: UserRepo, pass_word_service:PasswordService):
        self.user_repo = user_repo
        self.pass_word_service = pass_word_service

    def create_user(self, username: str, pass_word: str) -> User:
        self.pass_word_service.check_password_strength(pass_word=pass_word)
        salt = self.pass_word_service.create_salt()
        pass_word = self.pass_word_service.hash_password(pass_word, salt)
        user = self.user_repo.insert_into_db(username = username, salt = salt, hashed_password=pass_word)
        return(user)
    
    def login(self, username, pass_word):
        user_with_username: Optional[User] = self.user_repo.get_by_username(username=username)
        if user_with_username is None:
            raise Exception("Username incorect")
        self.pass_word_service.validate_password_salt(pass_word=pass_word, 
                    hashed_password=user_with_username.pass_word, salt=user_with_username.salt)
        return user_with_username
        

    def get_user_by_id(self, user_id: int) -> User | None:
        return self.user_repo.get_by_id(user_id)
    
    def get_user_by_username(self, username : str)-> User | None:
        return self.user_repo.get_by_username(username=username)

    def delete_user(self, user_id: int) -> None:
        return self.user_repo.delete_user(user_id)
    
    def search_user(self, username: str) -> User:
        user = self.user_repo.get_by_username(username=username)
        if user == None:
            raise Exception("This User didn't exist.")
        return user
    
    def user_exists(self, username: str) -> User:
        user = self.user_repo.get_by_username(username=username)
        return True if user else False


if __name__=='__main__':
    from freezegun import freeze_time
    import dotenv
    from src.DAO.DBConnector import DBConnector
    dotenv.load_dotenv()
    db_connector = DBConnector()
    user_repo = UserRepo(db_connector)
    user_service = UserService(user_repo)