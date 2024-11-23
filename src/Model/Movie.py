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


class APIMovie(Movie):
    following_vote_average: Optional[float] = None
    total_liked_following: Optional[int] = None





