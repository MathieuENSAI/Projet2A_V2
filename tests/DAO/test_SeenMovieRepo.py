from src.DAO.SeenMovieRepo import SeenMovieRepo
from src.DAO.DBConnector import DBConnector
from src.Model.SeenMovie import SeenMovie
import pytest

db_connector=DBConnector()

def test_get_by_id_none():
    seenmovierepo=SeenMovieRepo(db_connector)
    assert seenmovierepo.get_by_id(12222251525) is None

def test_get_by_id_result():
    seenmovierepo=SeenMovieRepo(db_connector)
    user = User()