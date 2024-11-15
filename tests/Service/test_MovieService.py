from unittest.mock import MagicMock

import pytest

from src.DAO.MovieGenreRepo import MovieGenreRepo
from src.DAO.MovieRepo import MovieRepo
from src.Model.Movie import Movie
from src.Service.MovieFromTMDService import MovieFromTMDService
from src.Service.MovieService import MovieService


@pytest.fixture
def movie_repo():
    """Fixture pour simuler le MovieRepo"""
    return MagicMock(MovieRepo)


@pytest.fixture
def movie_TMDB():
    """Fixture pour simuler le MovieFromTMDService"""
    return MagicMock(MovieFromTMDService)


@pytest.fixture
def movie_genre_repo():
    """Fixture pour simuler le MovieGenreRepo"""
    return MagicMock(MovieGenreRepo)


@pytest.fixture
def movie_service(movie_repo, movie_TMDB, movie_genre_repo):
    """Fixture pour créer une instance de MovieService"""
    return MovieService(
        movie_repo=movie_repo,
        movie_TMDB=movie_TMDB,
        movie_genre_repo=movie_genre_repo
    )


def test_get_by_id(movie_service, movie_repo, movie_TMDB):
    """Test de la méthode get_by_id"""

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


def test_get_by_id_movie_not_found_in_repo_but_found_in_tmdb(movie_service, movie_repo, movie_TMDB, movie_genre_repo):
    """Test de la méthode get_by_id lorsque le film est trouvé dans TMDB mais pas dans le repo"""

    # Simulation des données
    movie_id = 1
    movie_data = {
        'movie': Movie(id=movie_id, title="Test Movie TMDB"),
        'movie_genre': 'Action'
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


def test_get_by_id_movie_not_found_anywhere(movie_service, movie_repo, movie_TMDB):
    """Test de la méthode get_by_id lorsque le film n'est trouvé ni dans le repo ni dans TMDB"""

    # Simulation des retours
    movie_id = 1
    movie_repo.get_by_id.return_value = None
    movie_TMDB.get_by_id.return_value = None

    # Test de l'exception levée
    with pytest.raises(FileNotFoundError):
        movie_service.get_by_id(movie_id)


def test_get_by_title(movie_service, movie_repo, movie_TMDB):
    """Test de la méthode get_by_title"""

    # Simulation des données
    title = "Test Movie"
    movie = Movie(id=1, title=title)

    # Configuration des mocks
    movie_repo.get_by_title.return_value = [movie]
    movie_TMDB.search_movie.return_value = [{'movie': movie}]

    # Appel de la méthode
    result = movie_service.get_by_title(title)

    # Vérifications
    movie_repo.get_by_title.assert_called_once_with(title, None)
    movie_TMDB.search_movie.assert_called_once_with(title)
    assert movie in result


def test_get_by_genre(movie_service, movie_repo, movie_TMDB):
    """Test de la méthode get_by_genre"""

    # Simulation des données
    genre = "Action"
    movie = Movie(id=1, title="Action Movie")

    # Configuration des mocks
    movie_repo.get_by_genre.return_value = [movie]
    movie_TMDB.search_movie.return_value = [{'movie': movie}]

    # Appel de la méthode
    result = movie_service.get_by_genre(genre)

    # Vérifications
    movie_repo.get_by_genre.assert_called_once_with(genre, None)
    movie_TMDB.search_movie.assert_called_once_with(genre)
    assert movie in result


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