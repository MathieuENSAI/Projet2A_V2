from fastapi import APIRouter, HTTPException, status

from src.Model.Movie import Movie

from src.Service.MovieService import MovieService

from .init_app import movie_service

movie_router = APIRouter(prefix="/movies", tags=["Movies"])


@movie_router.get("/{tmdb_id}", status_code=status.HTTP_200_OK)
def get_movie_by_id(tmdb_id: int):
    try:
        my_movie = movie_service.get_by_id(tmdb_id)
        return my_movie
    except FileNotFoundError:
        raise HTTPException(
            status_code=404,
            detail="Movie with id [{}] not found".format(tmdb_id),
        ) from FileNotFoundError
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid request") from Exception

@movie_router.get("/search", status_code=status.HTTP_200_OK)
def search_movie(query: str,
                language = None, primary_release_year = None, 
                page = None, region = None, year = None):
    try:
        results = movie_service.search_id_movie(query,language,primary_release_year,page,region,year)
        return results
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid request") from Exception