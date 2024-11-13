from fastapi import APIRouter, Depends, HTTPException, status
from typing import TYPE_CHECKING, Annotated
from fastapi.security import HTTPAuthorizationCredentials
from .JWTBearer import JWTBearer
from src.Model.Movie import Movie
from .init_app import jwt_service, movie_service
import logging

movie_router = APIRouter(prefix="/movies", tags=["Movies"])

@movie_router.get("/{movie_id}", status_code=status.HTTP_200_OK)
def get_movie_by_id(movie_id: int, credentials: Annotated[HTTPAuthorizationCredentials, Depends(JWTBearer(partial_access_allowed=True))]):
    
    if credentials.get("restricted_access", False):
        user_id=None
    else :
        user_id = jwt_service.validate_user_jwt(credentials.credentials)
    try:
        movie = movie_service.get_by_id(movie_id, user_id)
        return movie
    except FileNotFoundError:
        raise HTTPException(
            status_code=404,
            detail=f"Movie with id [{movie_id}] not found",
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

@movie_router.get("/search/genre", status_code=status.HTTP_200_OK)
def get_movie_by_genre(genre: str):
    try:
        movies = movie_service.get_by_genre(genre)
        return movies
    except Exception as e:
        logging.error(f"Error occurred: {e}")
        raise HTTPException(status_code=400, detail=f"Invalid request: {e}") from e

@movie_router.get("/search/release_period", status_code=status.HTTP_200_OK)
def get_movie_by_release_period(start_release_date:str, end_release_date:str):
    try:
        movies = movie_service.get_by_release_period(start_release_date, end_release_date)
        return movies
    except Exception as e:
        logging.error(f"Error occurred: {e}")
        raise HTTPException(status_code=400, detail=f"Invalid request: {e}") from e

@movie_router.get("/search/lastest_released", status_code=status.HTTP_200_OK)
def get_lastest_released(number:int):
    try:
        movies = movie_service.get_lastest_released(number)
        return movies
    except Exception as e:
        logging.error(f"Error occurred: {e}")
        raise HTTPException(status_code=400, detail=f"Invalid request: {e}") from e
