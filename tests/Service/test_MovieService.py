from unittest.mock import MagicMock

import pytest

from src.DAO.MovieGenreRepo import MovieGenreRepo
from src.DAO.MovieRepo import MovieRepo
from src.Model.Movie import Movie
from src.Service.MovieFromTMDService import MovieFromTMDService
from src.Service.MovieService import MovieService


@pytest.fixture
def movie_service():
    """Fixture pour simuler MovieRepo, MovieFromTMDService, MovieGenreRepo et MovieService"""
    movie_repo=MagicMock(MovieRepo)
    movie_TMDB = MagicMock(MovieFromTMDService)
    movie_genre_repo = MagicMock(MovieGenreRepo)
    return MovieService(movie_repo, movie_TMDB, movie_genre_repo), movie_repo, movie_TMDB, movie_genre_repo

def test_get_by_id(movie_service):
    """Test de la méthode get_by_id"""
    movie_service, movie_repo, movie_TMDB, _= movie_service
    # Simulation des données
    movie_id = 1
    expected_movie = Movie(id=movie_id, title="Test Movie")

    # Configuration des mocks
    movie_repo.get_by_id.return_value = expected_movie
    movie_TMDB.get_by_id.return_value = None

    # Appel de la méthode
    result = movie_service.get_by_id(movie_id)

    # Vérifications
    movie_repo.get_by_id.assert_called_once_with(movie_id)
    movie_TMDB.get_by_id.assert_not_called()  # TMDB ne doit pas être appelé
    assert result == expected_movie


def test_get_by_id_movie_not_found_in_repo_but_found_in_tmdb(movie_service):
    """Test de la méthode get_by_id lorsque le film est trouvé dans TMDB mais pas dans le repo"""
    movie_service, movie_repo, movie_TMDB, movie_genre_repo= movie_service

    # Simulation des données
    movie_id = 1234821
    movie_data = {
        'movie': Movie(id=movie_id, title="Test Movie TMDB"),
        'movie_genre': {'id_movie':movie_id, 'genres':[{'id': 12, 'name': 'Adventure'}, {'id': 878, 'name': 'Science Fiction'}, {'id': 53, 'name': 'Thriller'}]}
    }

    # Configuration des mocks
    movie_repo.get_by_id.return_value = None  # Pas trouvé dans le repo
    movie_TMDB.get_by_id.return_value = movie_data  # Trouvé dans TMDB

    # Appel de la méthode
    result = movie_service.get_by_id(movie_id)

    # Vérifications
    movie_repo.get_by_id.assert_called_once_with(movie_id)
    movie_TMDB.get_by_id.assert_called_once_with(movie_id)
    movie_repo.insert_into_db.assert_called_once_with([movie_data['movie'].__dict__])
    movie_genre_repo.insert_into_db.assert_called_once_with([movie_data['movie_genre']])
    assert result == movie_data['movie']


def test_get_by_id_movie_not_found_anywhere(movie_service):
    """Test de la méthode get_by_id lorsque le film n'est trouvé ni dans le repo ni dans TMDB"""
    movie_service, movie_repo, movie_TMDB, movie_genre_repo= movie_service

    # Simulation des retours
    movie_id = 1
    movie_repo.get_by_id.return_value = None
    movie_TMDB.get_by_id.return_value = None
    
    # Appel de la méthode
    result = movie_service.get_by_id(movie_id)
    
    # Vérification
    movie_repo.get_by_id.assert_called_once_with(movie_id)
    movie_TMDB.get_by_id.assert_called_once_with(movie_id)
    movie_repo.insert_into_db.assert_not_called()
    movie_genre_repo.insert_into_db.assert_not_called()
    assert result==None


def test_get_by_title_all_movie_found_in_local_db(movie_service):
    """Test de la méthode get_by_title"""
    movie_service, movie_repo, movie_TMDB, _= movie_service

    # Simulation des données
    title = "Nindja"
    movies = [Movie(id=1, title=title), Movie(id=5, title=title + "blanc"), Movie(id=6, title=title + "noir"), Movie(id=8, title="Black"+title), Movie(id=12, title= "White"+ title)]

    # Configuration des mock
    movie_repo.get_by_title.return_value = movies

    # Appel de la méthode
    result = movie_service.get_by_title(title)

    # Vérifications
    movie_repo.get_by_title.assert_called_once_with(title, None)
    movie_TMDB.search_movie.assert_not_called()
    assert result==movies

def test_get_by_title_movies_found_in_local_less_five(movie_service):
    """Test de la méthode get_by_title"""
    movie_service, movie_repo, movie_TMDB, _= movie_service

    # Simulation des données
    title = "Nindja"
    movies_found_in_local_db = [Movie(id=1, title=title), Movie(id=5, title=title + "blanc")]
    movies_found_on_tmdb = [{'movie': Movie(id=5, title=title + "blanc"), "genre_movie":None}, {'movie': Movie(id=6, title=title + "noir"), "genre_movie":None}, {'movie': Movie(id=8, title="Black"+title), "genre_movie":None}, {'movie': Movie(id=12, title= "White"+ title), "genre_movie":None}]

    # Configuration des mock
    movie_repo.get_by_title.return_value = movies_found_in_local_db
    movie_TMDB.search_movie.return_value = movies_found_on_tmdb

    # Appel de la méthode
    result = movie_service.get_by_title(title)

    # Vérifications
    movie_repo.get_by_title.assert_called_once_with(title, None)
    movie_TMDB.search_movie.assert_called_once_with(title)
    assert result==[Movie(id=1, title=title), Movie(id=5, title=title + "blanc"), Movie(id=6, title=title + "noir"), Movie(id=8, title="Black"+title), Movie(id=12, title= "White"+ title)]

def test_get_by_genre_all_found_in_local_db(movie_service):
    """Test de la méthode get_by_genre"""
    movie_service, movie_repo, movie_TMDB, _= movie_service

    # Simulation des données
    genre = "action"
    movies = [Movie(id=1), Movie(id=5), Movie(id=6), Movie(id=8), Movie(id=12)]

    # Configuration des mock
    movie_repo.get_by_genre.return_value = movies

    # Appel de la méthode
    result = movie_service.get_by_genre(genre)

    # Vérifications
    movie_repo.get_by_genre.assert_called_once_with(genre, None)
    movie_TMDB.search_movie.assert_not_called()
    assert result==movies

def test_get_by_genre_movies_found_in_local_less_five(movie_service):
    """Test de la méthode get_by_genre"""
    movie_service, movie_repo, movie_TMDB, _= movie_service

    # Simulation des données
    genre = "Action"
    movies_found_in_local_db = [Movie(id=1), Movie(id=5)]
    movies_found_on_tmdb = [{'movie': Movie(id=5), "genre_movie":None}, {'movie': Movie(id=6), "genre_movie":None}, {'movie': Movie(id=8), "genre_movie":None}, {'movie': Movie(id=12), "genre_movie":None}]

    # Configuration des mock
    movie_repo.get_by_genre.return_value = movies_found_in_local_db
    movie_TMDB.search_movie.return_value = movies_found_on_tmdb

    # Appel de la méthode
    result = movie_service.get_by_genre(genre)

    # Vérifications
    movie_repo.get_by_genre.assert_called_once_with(genre, None)
    movie_TMDB.search_movie.assert_called_once_with(genre)
    assert result==[Movie(id=1), Movie(id=5), Movie(id=6), Movie(id=8), Movie(id=12)]


def test_get_by_release_period(movie_service, movie_repo, movie_TMDB):
    """Test de la méthode get_by_release_period"""

    # Simulation des données
    start_date = "2020-01-01"
    end_date = "2020-12-31"
    movie = Movie(id=1, title="Released Movie")

    # Configuration des mocks
    movie_repo.get_by_release_period.return_value = [movie]
    movie_TMDB.get_by_release_period.return_value = [{'movie': movie}]

    # Appel de la méthode
    result = movie_service.get_by_release_period(start_date, end_date)

    # Vérifications
    movie_repo.get_by_release_period.assert_called_once_with(start_date, end_date)
    movie_TMDB.get_by_release_period.assert_called_once_with(start_date, end_date)
    assert movie in result


def test_get_lastest_released(movie_service, movie_TMDB, movie_repo, movie_genre_repo):
    """Test de la méthode get_lastest_released"""

    # Simulation des données
    number = 5
    movie = Movie(id=1, title="Latest Movie")
    movies_data = [{'movie': movie, 'movie_genre': 'Action'}]

    # Configuration des mocks
    movie_TMDB.get_lastest_released.return_value = movies_data

    # Appel de la méthode
    result = movie_service.get_lastest_released(number)

    # Vérifications
    movie_TMDB.get_lastest_released.assert_called_once_with(number)
    movie_repo.insert_into_db.assert_called_once_with([movie.__dict__])
    movie_genre_repo.insert_into_db.assert_called_once_with([movies_data[0]['movie_genre']])
    assert movie in result