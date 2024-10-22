from pydantic import BaseModel
from datetime import date

class Movie(BaseModel):
    id : int
    original_language: str=None
    original_title: str=None
    release_date:date=None
    title:str=None
    vote_average: float=None
    vote_count: int=None
    overview: str=None

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






