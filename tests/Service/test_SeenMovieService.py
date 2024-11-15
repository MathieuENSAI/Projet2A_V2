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

def test_add_to_watchlist_new():
    user = User(id_user=1,username="Emile",pass_word="Emilemdp", salt=None)
    movie = Movie(id=17)
    seenmovierepo=SeenMovieRepo(MockDBConnector())
    seenmovieservice = SeenMovieService(seenmovierepo)
    db = seenmovierepo.db_connector.db
    seenmovie : SeenMovie = seenmovieservice.add_to_watchlist(user.id_user,movie.id)
    assert seenmovie is not None
    assert seenmovie.__dict__ == db[-1]
    assert seenmovie.id_user == 1
    assert seenmovie.id_movie == 17
    assert seenmovie.seen == False
    assert seenmovie.vote == None
    assert seenmovie.favorite == False

def test_add_to_favoritelist_new():
    user = User(id_user=1,username="Emile",pass_word="Emilemdp", salt=None)
    movie = Movie(id=17)
    seenmovierepo=SeenMovieRepo(MockDBConnector())
    seenmovieservice = SeenMovieService(seenmovierepo)
    db = seenmovierepo.db_connector.db
    seenmovie : SeenMovie = seenmovieservice.add_to_favoritelist(user.id_user,movie.id)
    assert seenmovie is not None
    assert seenmovie.__dict__ == db[-1]
    assert seenmovie.id_user == 1
    assert seenmovie.id_movie == 17
    assert seenmovie.seen == True
    assert seenmovie.vote == None
    assert seenmovie.favorite == True

#def test_delete_seenmovie_by_user_and_movie():

def test_watchlist_exist():
    seenmovierepo=SeenMovieRepo(MockDBConnector())
    seenmovieservice = SeenMovieService(seenmovierepo)
    list_movies : list[Movie] = seenmovieservice.watchlist(id_user=1)
    assert list_movies[0] == Movie(id=5)
    assert list_movies[1] == Movie(id=6)

def test_favorite_movie_user_exist():
    seenmovierepo=SeenMovieRepo(MockDBConnector())
    seenmovieservice = SeenMovieService(seenmovierepo)
    list_movies : list[Movie] = seenmovieservice.favorite_movie_user(id_user=4)
    assert list_movies is not None
    assert list_movies[0] == Movie(id=1)

def test_seenmovies_user_exist():
    seenmovierepo=SeenMovieRepo(MockDBConnector())
    seenmovieservice = SeenMovieService(seenmovierepo)
    list_movies : list[Movie] = seenmovieservice.seenmovies_user(id_user=4)
    assert list_movies is not None
    assert list_movies[0] == Movie(id=3)
    assert list_movies[1] == Movie(id=2)
    assert list_movies[2] == Movie(id=1)

def test_movie_seen_by():
    seenmovierepo=SeenMovieRepo(MockDBConnector())
    seenmovieservice = SeenMovieService(seenmovierepo)
    users : list[User] = seenmovieservice.movie_seen_by(1)
    assert users is not None
    assert users[0].id_user == 3
    assert users[0].username == ""
    assert users[0].pass_word == ""
    assert users[0].salt is None
    assert users[0] == User(id_user=3, username="",pass_word="", salt=None)
    assert users[1] == User(id_user=5, username="",pass_word="", salt=None)
    assert users[2] == User(id_user=4, username="",pass_word="", salt=None)
