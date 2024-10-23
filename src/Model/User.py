from pydantic import BaseModel


class User(BaseModel):
    id_user : int | None
    username: str 
    pass_word: str
    salt: str
    following : list[int] = []
    favorite_movie : list[int] = []
    watchlist : list[int] = []


    # def follow(self, user):
    #     following.append(user(id))
    #     return self.following
    
    # def stop_follow(self, username):
    #     ##TODO
    
    # def add_favorite_movie(self, movie_title):
    #     ##TODO
        
    


        