from pydantic import BaseModel

class SeenMovie(BaseModel):
    id_user : int 
    id_movie : int 
    seen : bool 
    vote : int = None 
    favorite : bool = False