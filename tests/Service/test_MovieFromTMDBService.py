import pytest
from src.Service.MovieFromTMDService import MovieFromTMDService

def test_init():
    movie_db = MovieFromTMDService()
    assert movie_db.header == {
    "accept": "application/json",
    "Authorization": "Bearer "+ "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIxMTdjYzRlYzBjY2VjODAyYjhkODNkZGU4NDkyZDcxZCIsIm5iZiI6MTcyOTY3NjU1OS45OTA4Mywic3ViIjoiNjZkYjEyMTA4YmE4MDk1NDE1MTYwYzhkIiwic2NvcGVzIjpbImFwaV9yZWFkIl0sInZlcnNpb24iOjF9.xrY10i-l9xXzCW6CKuZsF52RyRsw1--N0c5s9Q-M7MI"
    }

def test_get_by_id_exist():
    movie_db = MovieFromTMDService()
    movie = movie_db.get_by_id(1234821)
    assert movie['movie'].id==1234821
    assert movie['movie_genre']['id_movie']==1234821
    assert movie['movie_genre']['genres']==[{'id': 12, 'name': 'Adventure'}, {'id': 878, 'name': 'Science Fiction'}, {'id': 53, 'name': 'Thriller'}]

def test_get_by_id_not_exist():
    movie_db = MovieFromTMDService()
    movie = movie_db.get_by_id(1)
    assert movie==None

def test_search_movie_found():
    movie_db = MovieFromTMDService()
    movies = movie_db.search_movie("Something Was in the Tunnels")
    assert movies[0]['movie'].id==1370676
    assert movies[0]['movie_genre']['id_movie']==1370676
    assert movies[0]['movie_genre']['genres']==[27, 9648, 18, 53]

def test_search_movie_no_found():
    movie_db = MovieFromTMDService()
    movies = movie_db.search_movie("Nindja")
    assert movies==[]

def test_get_by_release_period_found():
    movie_db = MovieFromTMDService()
    movies = movie_db.get_by_release_period('2025-07-01', '2025-07-02')
    assert '2025-07-01' <= movies[0]['movie'].release_date <= '2025-07-02'
    assert '2025-07-01' <= movies[-1]['movie'].release_date <= '2025-07-02'
    assert movies[0]['movie'].id==1234821
    assert movies[0]['movie_genre']['id_movie']==1234821
    assert movies[0]['movie_genre']['genres']==[12, 878, 53]
    assert movies[-1]['movie'].id==1355815
    assert movies[-1]['movie_genre']['id_movie']==1355815
    assert movies[-1]['movie_genre']['genres']==[53, 80]

def test_get_by_release_period_no_found():
    movie_db = MovieFromTMDService()
    movies = movie_db.get_by_release_period('2025-07-02', '2025-07-01')
    assert movies==[]
    
def test_get_lastest_released():
    movie_db = MovieFromTMDService()
    movies = movie_db.get_lastest_released(5)
    assert len(movies)==5
    # assert movies[0]['movie'].id==1391783 ## Donnée changeant au cours du temps
    # assert movies[0]['movie'].release_date=='2024-11-22' ## Donnée changeant au cours du temps


def test_get_id_name_genre():
    movie_db = MovieFromTMDService()
    genres = movie_db.get_id_name_genre()
    # assert genres[0].id_genre==28
    # assert genres[0].name_genre=='Action'
    # assert genres[-1].id_genre==37
    # assert genres[-1].name_genre=='Western'