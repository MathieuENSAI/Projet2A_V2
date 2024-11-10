from pydantic import BaseModel
from typing import Optional

class SeenMovie(BaseModel):
    id_user : int 
    id_movie : int 
    seen : bool 
    vote : Optional[int] = None 
    favorite : bool = False