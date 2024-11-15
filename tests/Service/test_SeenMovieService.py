from tests.DAO.test_SeenMovieRepo import MockDBConnector
from typing import TYPE_CHECKING, Literal, Optional, Union
from src.Model.SeenMovie import SeenMovie
from src.Model.Movie import Movie
from src.Model.User import User
from src.Service.SeenMovieService import SeenMovieService
from src.DAO.SeenMovieRepo import SeenMovieRepo

if TYPE_CHECKING:
    from src.Model.SeenMovie import SeenMovie

def test_seen_movie():
    user = User(id_user=1,username="Emile",pass_word="Emilemdp", salt=None)
    movie = Movie(id=5)
    seenmovierepo=SeenMovieRepo(MockDBConnector())
    seenmovieservice = SeenMovieService(seenmovierepo)
    db = seenmovierepo.db_connector.db
    seenmovie : SeenMovie = seenmovieservice.seen_movie(user.id_user,movie.id)
    assert seenmovie is not None
    assert seenmovie.__dict__ == db[-1]
    assert seenmovie.id_user == 1
    assert seenmovie.id_movie == 5
    assert seenmovie.seen == True
    assert seenmovie.vote == None
    assert seenmovie.favorite == False

def test_add_to_watchlist():
    user = User(id_user=1,username="Emile",pass_word="Emilemdp", salt=None)
    movie = Movie(id=17)
    seenmovierepo=SeenMovieRepo(MockDBConnector())
    seenmovieservice = SeenMovieService(seenmovierepo)
    db = seenmovierepo.db_connector.db
    seenmovie : SeenMovie = seenmovieservice.add_to_watchlist(user,movie)
    assert seenmovie is not None
    assert seenmovie.__dict__ == db[-1]
    assert seenmovie.id_user == 1
    assert seenmovie.id_movie == 17
    assert seenmovie.seen == False
    assert seenmovie.vote == None
    assert seenmovie.favorite == False