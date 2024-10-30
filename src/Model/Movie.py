from pydantic import BaseModel
from datetime import date

class Movie(BaseModel):
    id : int
    original_language: str|None=None
    original_title: str|None=None
    release_date:date|str|None=None
    title:str|None=None
    vote_average: float|None=None
    vote_count: int|None=None
    overview: str|None=None

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

if __name__ == "__main__" :
   movie= Movie(id=1)
   print(movie.__dict__)





