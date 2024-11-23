from unittest.mock import MagicMock
import pytest
from src.DAO.MovieRepo import MovieRepo
from src.DAO.SeenMovieRepo import SeenMovieRepo
from src.Service.Noteservice  import NoteService
from src.Model.User import User 
from src.Model.Movie import Movie 


@pytest.fixture
def note_service():
    """Fixture pour simuler MovieRepo, SeenMovieRepo et NoteService"""
    movie_repo=MagicMock(MovieRepo)
    seen_movie_repo = MagicMock(SeenMovieRepo)
    return NoteService(movie_repo, seen_movie_repo), seen_movie_repo, movie_repo

def test_note_movie(note_service):
    note_service, seen_movie_repo, movie_repo = note_service
    # Simulation des données
    id_user, id_movie, note=1, 1, 9
    expected_movie = Movie(id=id_movie)
    
    # Configuration des mocks
    seen_movie_repo.note_movie.return_value = {"vote_avg":8, "vote_count":2}
    movie_repo.update_vote.return_value = expected_movie

    # Appel de la méthode
    result = note_service.note_movie(id_user, id_movie, note)

    # Vérifications
    seen_movie_repo.note_movie.assert_called_once_with(id_user, id_movie, note)
    movie_repo.update_vote.assert_called_once_with(id_movie, 8, 2)
    assert result == expected_movie

def test_remove_note_movie(note_service):
    note_service, seen_movie_repo, movie_repo = note_service
    # Simulation des données
    id_user, id_movie = 1, 2
    expected_movie = Movie(id=id_movie)
    
    # Configuration des mocks
    seen_movie_repo.remove_note_movie.return_value = {"vote_avg":8, "vote_count":2}
    movie_repo.update_vote.return_value = expected_movie

    # Appel de la méthode
    result = note_service.remove_note_movie(id_user, id_movie)

    # Vérifications
    seen_movie_repo.remove_note_movie.assert_called_once_with(id_user, id_movie)
    movie_repo.update_vote.assert_called_once_with(id_movie, 8, 2)
    assert result == expected_movie
