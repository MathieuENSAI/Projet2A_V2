from pydantic import BaseModel
from datetime import date

class Movie(BaseModel):
    id_movie: int
    original_title: str
    data_sortie: date
    realisateur: str
    langue_vo: str
    genre: str
    resume: str
    note_moyenne: str
    



