from pydantic import BaseModel
from datetime import date
from typing import Optional

class Movie(BaseModel):
    id : int
    original_language: Optional[str]=None
    original_title: Optional[str]=None
    release_date:Optional[date|str]=None
    title: Optional[str]=None
    vote_average: Optional[float]=None
    vote_count: Optional[int]=None
    overview: Optional[str]=None


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

class APIMovie(Movie):
    following_vote_average: Optional[float] = None
    total_liked_following: Optional[int] = None

if __name__ == "__main__" :
   movie= Movie(id=1)
   print(movie.__dict__)





