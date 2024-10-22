from pydantic import BaseModel

class SeenMovie(BaseModel):
    id_seenmovie : int | None
    id_user : int 
    id_movie : int 
    seen : bool 
    note : int = None 
    favorite : bool = False