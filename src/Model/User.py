from pydantic import BaseModel
# from src.Service.UserService import UserService
# from src.Service.MovieService import MovieService


class User(BaseModel):
    id_user : int|None=None
    username: str 
    pass_word: str
    salt: str|None
    following : list[int] = []
    favorite_movie : list[int] = []
    watchlist : list[int] = []


    # def follow(self, user):
    #     following.append(user(id))
    #     return self.following
    # def follow(self, user):
    #     following.append(user(id))
    #     return self.following
    
    # def stop_follow(self, username):
    #     ##TODO
    # def stop_follow(self, username):
    #     ##TODO
    
    # def add_favorite_movie(self, movie_title):
    #     ##TODO
    # def add_favorite_movie(self, movie_title):
        ##TODO
    # def add_favorite_movie(self, movie_title):
    #     ##TODO