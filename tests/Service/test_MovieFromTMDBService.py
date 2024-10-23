import pytest

from src.Service.MovieFromTMDService import MovieFromTMDService

def test_init():
    movie_db = MovieFromTMDService(None)
    assert movie_db.movie_db is None

def test_get_by_id(id_movie):
    movie_db = MovieFromTMDService(None)
    movie = movie_db.get_by_id(id_movie)
    assert movie.id==id_movie
    


