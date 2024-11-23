from fastapi import APIRouter, Depends, HTTPException, status
from typing import TYPE_CHECKING, Annotated
from fastapi.security import HTTPAuthorizationCredentials
from .JWTBearer import JWTBearer
from src.Model.Movie import Movie
from .init_app import jwt_service, user_service, movie_service
import logging
from pydantic import BaseModel, Field
from datetime import date

movie_router = APIRouter(prefix="/movies", tags=["Movies"])

@movie_router.get("/{movie_id}", status_code=status.HTTP_200_OK, summary="Search for a movie by Id")
def get_movie_by_id(movie_id: int, credentials: Annotated[HTTPAuthorizationCredentials, Depends(JWTBearer(partial_access_allowed=True))]):
    """ 
    Search for a movie using its unique identifier. Basic information is accessible to all users, while authenticated users with a valid token can access additional details.
    """
    try:
        user_id = jwt_service.validate_user_jwt(credentials.credentials)  
        # Authentification renforcé au niveau backend en plus de jwt
        if not user_service.is_connected(user_id):
            raise HTTPException(status_code=404, detail="It seem like you are no longer connected.")
    except Exception :
        user_id=None
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

@movie_router.get("/search/title/{title}", status_code=status.HTTP_200_OK, summary="Search for a movie by title")
def get_movie_by_title(title: str, credentials: Annotated[HTTPAuthorizationCredentials, Depends(JWTBearer(partial_access_allowed=True))]):
    """ 
     Find movies by providing their title. Unauthenticated users can access basic details, while authenticated users with a valid token can view more comprehensive information.
    """
    try:
        user_id = jwt_service.validate_user_jwt(credentials.credentials) 
        # Authentification renforcé au niveau backend en plus de jwt
        if not user_service.is_connected(user_id):
            raise HTTPException(status_code=404, detail="It seem like you are no longer connected.") 
    except Exception :
        user_id=None
    try:
        movies = movie_service.get_by_title(title, user_id)
        return movies
    except Exception as e:
        logging.error(f"Error occurred: {e}")
        raise HTTPException(status_code=400, detail=f"Invalid request: {e}") from e

@movie_router.get("/search/genre/{genre}", status_code=status.HTTP_200_OK, summary="Search for movies by genre")
def get_movie_by_genre(genre: str, credentials: Annotated[HTTPAuthorizationCredentials, Depends(JWTBearer(partial_access_allowed=True))]):
    """ 
    This route lets you explore movies within a specific genre. Partial access is available without authentication, providing basic information about the movies. However, to view more detailed information, a valid authentication token is required.
    """
    try:
        user_id = jwt_service.validate_user_jwt(credentials.credentials)  
        # Authentification renforcé au niveau backend en plus de jwt
        if not user_service.is_connected(user_id):
            raise HTTPException(status_code=404, detail="It seem like you are no longer connected.")
    except Exception :
        user_id=None
    try:
        movies = movie_service.get_by_genre(genre, user_id)
        return movies
    except Exception as e:
        logging.error(f"Error occurred: {e}")
        raise HTTPException(status_code=400, detail=f"Invalid request: {e}") from e

class ReleasePeriod(BaseModel): 
    start: date
    end: date 

@movie_router.get("/search/release_period", status_code=status.HTTP_200_OK, summary="Search for movies by release period")
def get_movie_by_release_period(release_period:ReleasePeriod=Depends(ReleasePeriod)):
    """ 
    This route allows you to search for movies within a specified release period. By providing a start and end date, you can retrieve movies released within that timeframe.
    """
    try:
        movies = movie_service.get_by_release_period(release_period.start, release_period.end)
        return movies
    except Exception as e:
        logging.error(f"Error occurred: {e}")
        raise HTTPException(status_code=400, detail=f"Invalid request: {e}") from e

@movie_router.get("/search/lastest_released/{number}", status_code=status.HTTP_200_OK, summary="Retrieve the latest released movies")
def get_lastest_released(number:int):
    """ 
    This endpoint retrieves the most recently released movies. You can specify the number of movies you want to receive by providing the number parameter in the URL. The movies are returned in descending order of their release date, ensuring you get the latest releases first.
    """
    try:
        movies = movie_service.get_lastest_released(number)
        return movies
    except Exception as e:
        logging.error(f"Error occurred: {e}")
        raise HTTPException(status_code=400, detail=f"Invalid request: {e}") from e
