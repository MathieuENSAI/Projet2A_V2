from pydantic import BaseModel
from typing import Optional


class User(BaseModel):
    id_user : int
    username: str 
    salt: Optional[str]=""
    pass_word: Optional[str]=""
    following : Optional[list[int]] = []
    favorite_movie : Optional[list[int]] = []
    watchlist : Optional[list[int]] = []
