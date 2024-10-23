from src.DAO.SeenMovieRepo import SeenMovieRepo
from src.DAO.DBConnector import DBConnector
from src.Model.SeenMovie import SeenMovie
import pytest

db_connector=DBConnector()

# def test_get_by_id_none():
#     seenmovierepo=SeenMovieRepo(db_connector)
#     assert seenmovierepo.get_by_id(12222251525) is None

# def test_get_by_id_result():
#     seenmovierepo=SeenMovieRepo(db_connector)
#     seenmovie = SeenMovie(id_seenmovie=1, 
#                           id_user=1, id_movie=1,seen=True,
#                           vote=8,favorite=True)
#     assert seenmovie == seenmovierepo.get_by_id(1)

def test_get_by_user_and_movie_none():
    seenmovierepo=SeenMovieRepo(db_connector)
    assert seenmovierepo.get_by_user_and_movie(12222251525,444) is None

def test_get_by_user_and_movie_result():
    seenmovierepo=SeenMovieRepo(db_connector)
    seenmovie = SeenMovie(id_seenmovie=1, 
                          id_user=1, id_movie=1,seen=True,
                          vote=8,favorite=True)
    assert seenmovie == seenmovierepo.get_by_user_and_movie(1,1)

def test_insert_into_db_sucess():
    seenmovierepo=SeenMovieRepo(db_connector)
    seenmovie = SeenMovie(id_user=1, id_movie=3,seen=True, vote=1, favorite=True)
    assert seenmovie == seenmovierepo.insert_into_db(
                          id_user=1, id_movie=3,seen=True, vote=1, favorite=True)

def test_insert_into_db_fail():
    seenmovierepo=SeenMovieRepo(db_connector)
    seenmovie = SeenMovie(id_user=1, id_movie=3,seen=True, vote=1, favorite=True)
    assert seenmovie != seenmovierepo.insert_into_db(id_user=1, id_movie=3,
                                                     seen=True, vote=1, favorite=True)
    
def test_delete_from_db_success():
    seenmovierepo=SeenMovieRepo(db_connector)
    seenmovie = SeenMovie(id_user=1, id_movie=3,seen=True, vote=1, favorite=True)
    assert seenmovierepo.delete_from_db(seenmovie) == True

def test_update_db():
    seenmovierepo=SeenMovieRepo(db_connector)
    seenmovie = SeenMovie(id_user=1, id_movie=3,seen=True, vote=2, favorite=True)
    assert seenmovierepo.update_db(seenmovie) == True


def test_get_list_seenmovies_by_user_none():
    seenmovierepo=SeenMovieRepo(db_connector)
    assert seenmovierepo.get_list_seenmovies_by_user(15) is None

def test_get_list_seenmovies_by_user_sucess():
    seenmovierepo=SeenMovieRepo(db_connector)
    assert seenmovierepo.get_list_seenmovies_by_user(1) == [1,2,3]
