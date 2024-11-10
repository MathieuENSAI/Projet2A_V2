from fastapi import APIRouter, Depends, HTTPException, status
from typing import TYPE_CHECKING, Annotated
from fastapi.security import HTTPAuthorizationCredentials
from .JWTBearer import JWTBearer
from src.Model.Movie import Movie
from src.Model.SeenMovie import SeenMovie
from .init_app import jwt_service, movie_service, seen_movie_service, note_service
import logging

watch_movie_route = APIRouter(prefix="/watch", tags=["Watch Movies"])

@watch_movie_route.get("/{movie_id}", status_code=status.HTTP_200_OK, dependencies=[Depends(JWTBearer())])
def watch_movie(movie_id: int, credentials: Annotated[HTTPAuthorizationCredentials, Depends(JWTBearer())]):
    user_id = jwt_service.validate_user_jwt(credentials.credentials)
    movie = movie_service.get_by_id(movie_id)
    if movie is None:
        raise HTTPException(status_code=404, detail="Movie with this id does not exist.")
    try:
        seen_movie = seen_movie_service.seen_movie(user_id, movie_id)
    except Exception:
        raise HTTPException(status_code=409, detail="Something is going wrong. Try again !") from Exception
    return movie

@watch_movie_route.get("/add-to-watch-list/{movie_id}", status_code=status.HTTP_200_OK, dependencies=[Depends(JWTBearer())])
def add_to_watchlist(movie_id: int, credentials: Annotated[HTTPAuthorizationCredentials, Depends(JWTBearer())]):
    user_id = jwt_service.validate_user_jwt(credentials.credentials)
    movie = movie_service.get_by_id(movie_id)
    if movie is None:
        raise HTTPException(status_code=404, detail="Movie with this id does not exist.")
    try:
        movie_to_watch_later = seen_movie_service.add_to_watchlist(user_id, movie_id)
    except Exception:
        raise HTTPException(status_code=409, detail="Something is going wrong. Try again !") from Exception
    return movie

@watch_movie_route.get("/add-to-favorite-list/{movie_id}", status_code=status.HTTP_200_OK, dependencies=[Depends(JWTBearer())])
def add_to_favoritelist(movie_id: int, credentials: Annotated[HTTPAuthorizationCredentials, Depends(JWTBearer())]):
    user_id = jwt_service.validate_user_jwt(credentials.credentials)
    movie = movie_service.get_by_id(movie_id)
    if movie is None:
        raise HTTPException(status_code=404, detail="Movie with this id does not exist.")
    try:
        movie_to_favoritelist = seen_movie_service.add_to_favoritelist(user_id, movie_id)
    except Exception:
        raise HTTPException(status_code=409, detail="Something is going wrong. Try again !") from Exception
    return movie
