from fastapi import APIRouter, HTTPException, status

from src.Model.Movie import Movie

from .init_app import movie_service

import logging

movie_router = APIRouter(prefix="/movies", tags=["Movies"])


@movie_router.get("/{movie_id}", status_code=status.HTTP_200_OK)
def get_movie_by_id(movie_id: int):
    try:
        my_movie = movie_service.get_by_id(movie_id)
        return my_movie
    except FileNotFoundError:
        raise HTTPException(
            status_code=404,
            detail="Movie with id [{}] not found".format(movie_id),
        ) from FileNotFoundError
    except Exception as e:
        logging.error(f"Error occurred: {e}")
        raise HTTPException(status_code=400, detail=f"Invalid request: {e}") from e

@movie_router.get("/search/title", status_code=status.HTTP_200_OK)
def get_movie_by_title(title: str):
    try:
        movies = movie_service.get_by_title(title)
        return movies
    except Exception as e:
        logging.error(f"Error occurred: {e}")
        raise HTTPException(status_code=400, detail=f"Invalid request: {e}") from e

@movie_router.get("/search/release_date", status_code=status.HTTP_200_OK)
def get_movie_by_release_date(release_date: str):
    try:
        movies = movie_service.get_by_release_date(release_date)
        return movies
    except Exception as e:
        logging.error(f"Error occurred: {e}")
        raise HTTPException(status_code=400, detail=f"Invalid request: {e}") from e
