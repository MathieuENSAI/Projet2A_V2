from pydantic import BaseModel

class MovieGenre(BaseModel):
    id_genre : int
    id_movie: int

