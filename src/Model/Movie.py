from pydantic import BaseModel
from datetime import date

class Movie(BaseModel):
    id : int
    original_language: str
    original_title: str
    release_date:date
    titre:str
    vote_average: float
    vote_count: int
    overview: str

    # def update_average_rating(self):

    def info(self):
        info = f"""
        id: {self.id}
        original_language: {self.original_language}
        original_title: {self.original_title}
        release_date: {self.release_date}
        titre: {self.titre}
        vote_average: {self.vote_average}
        vote_count: {self. vote_count}
        overview: {self.overview}
        """

        return info






