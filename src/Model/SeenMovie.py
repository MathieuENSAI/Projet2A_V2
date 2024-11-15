from pydantic import BaseModel

class SeenMovie(BaseModel):
    id_user : int 
    id_movie : int 
    seen : bool 
    to_watch_later: bool
    vote : int|None = None 
    favorite : bool = False