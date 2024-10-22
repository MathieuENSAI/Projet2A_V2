from pydantic import BaseModel
from datetime import date

class Movie(BaseModel):
    movie_id : int
    original_title: str
    date_sortie: date
    realisateur: str
    langue_vo: str
    genre: str
    resume: str
    average_rating: str = None

    # def update_average_rating(self):

    def info(self):
        info = f"""
        id_movie: {self.id_movie}
        original_title: {self.original_title}
        date_sortie: {self.date}
        realisateur: {self.realisateur}
        langue_vo: {self.langue_vo}
        genre: {self.genre}
        resume: {self.re}
        average_rating: {self.average_rating}
        """

        return info






