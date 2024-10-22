from pydantic import BaseModel


class User(BaseModel):
    id_user : int
    username: str
    pass_word: str
    salt: str