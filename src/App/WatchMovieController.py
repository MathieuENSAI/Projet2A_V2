from pydantic import BaseModel, conint
from fastapi import APIRouter, Depends, HTTPException, status, Body
from typing import TYPE_CHECKING, Annotated
from fastapi.security import HTTPAuthorizationCredentials
from .JWTBearer import JWTBearer
from src.Model.Movie import Movie
from src.Model.SeenMovie import SeenMovie
from .init_app import jwt_service, user_service, movie_service, seen_movie_service, note_service
import logging

watch_movie_route = APIRouter(prefix="/watch", tags=["Watch Movies"])

@watch_movie_route.get("/{movie_id}", status_code=status.HTTP_200_OK, dependencies=[Depends(JWTBearer())], summary="Watch a movie")
def watch_movie(movie_id: int, credentials: Annotated[HTTPAuthorizationCredentials, Depends(JWTBearer())]):
    """ 
    This action allows you to watch a movie. Authentication is required, and the movie must exist in the database. A valid token is needed to perform this action and access the movie.
    """
    user_id = jwt_service.validate_user_jwt(credentials.credentials)
    # Authentification renforcé au niveau backend en plus de jwt
    if not user_service.is_connected(user_id):
        raise HTTPException(status_code=404, detail="It seem like you are no longer connected.")
    movie = movie_service.get_by_id(movie_id)
    if movie is None:
        raise HTTPException(status_code=404, detail="Movie with this id does not exist.")
    try:
        seen_movie = seen_movie_service.watch_movie(user_id, movie_id)
    except Exception:
        raise HTTPException(status_code=500, detail="Something is going wrong. Try again !") from Exception
    return movie

@watch_movie_route.get("/watch/get_seen_movies", status_code=status.HTTP_200_OK, dependencies=[Depends(JWTBearer())], summary="The movies you have seen.")
def get_seen_list(credentials: Annotated[HTTPAuthorizationCredentials, Depends(JWTBearer())]):
    """ 
    This action allows you to get your list of movies you have seen. Authentication is required. A valid token is needed to perform this action and access the watchlist.
    """
    user_id = jwt_service.validate_user_jwt(credentials.credentials)
    # Authentification renforcé au niveau backend en plus de jwt
    if not user_service.is_connected(user_id):
        raise HTTPException(status_code=404, detail="It seem like you are no longer connected.")
    try:
        seenlist = seen_movie_service.user_seenmovies(user_id)
    except Exception:
        raise HTTPException(status_code=500, detail="Something is going wrong. Try again !") from Exception
    return seen_movie_service.user_seenmovies(user_id)

@watch_movie_route.post("/add-to-watch-lists", status_code=status.HTTP_200_OK, dependencies=[Depends(JWTBearer())], summary="Add a movie to your watchlist")
def add_to_watchlist(movie_id: int, credentials: Annotated[HTTPAuthorizationCredentials, Depends(JWTBearer())]):
    """ 
    To add a movie to your watchlist, authentication is required. This feature lets you save movies for later viewing, helping you keep track of films you'd like to watch in the future.
    """
    user_id = jwt_service.validate_user_jwt(credentials.credentials)
    # Authentification renforcé au niveau backend en plus de jwt
    if not user_service.is_connected(user_id):
        raise HTTPException(status_code=404, detail="It seem like you are no longer connected.")
    movie = movie_service.get_by_id(movie_id)
    if movie is None:
        raise HTTPException(status_code=404, detail="Movie with this id does not exist.")
    try:
        movie_to_watch_later = seen_movie_service.add_to_watchlist(user_id, movie_id)
    except Exception:
        raise HTTPException(status_code=500, detail="Something is going wrong. Try again !") from Exception
    return movie

@watch_movie_route.get("/watchlist/get_watch_list", status_code=status.HTTP_200_OK, dependencies=[Depends(JWTBearer())], summary="Your watchlist")
def get_watch_list(credentials: Annotated[HTTPAuthorizationCredentials, Depends(JWTBearer())]):
    """ 
    This action allows you to get your list of movies you have planed to watch. Authentication is required. A valid token is needed to perform this action and access the watchlist.
    """
    user_id = jwt_service.validate_user_jwt(credentials.credentials)
    # Authentification renforcé au niveau backend en plus de jwt
    if not user_service.is_connected(user_id):
        raise HTTPException(status_code=404, detail="It seem like you are no longer connected.")
    try:
        watchlist = seen_movie_service.user_watchlist(user_id)
    except Exception:
        raise HTTPException(status_code=500, detail="Something is going wrong. Try again !") from Exception
    return seen_movie_service.user_watchlist(user_id)

@watch_movie_route.put("/remove-from-watchlist/{movie_id}", status_code=status.HTTP_200_OK, dependencies=[Depends(JWTBearer())], summary="")
def remove_from_user_watchlist(movie_id:int, credentials: Annotated[HTTPAuthorizationCredentials, Depends(JWTBearer())]):
    """
    This action allows you to remove a movie from your watchlist. Note that a valid token is required to perform this operation.
    """
    user_id = jwt_service.validate_user_jwt(credentials.credentials)
    return seen_movie_service.remote_from_user_watchlists(user_id, movie_id)

@watch_movie_route.post("/add-to-favorite-lists", status_code=status.HTTP_200_OK, dependencies=[Depends(JWTBearer())], summary="Add a movie to your favorite list")
def add_to_favoritelist(movie_id: int, credentials: Annotated[HTTPAuthorizationCredentials, Depends(JWTBearer())]):
    """
    Authenticated users can save a movie to their favorites list using its unique ID. This feature allows users to easily track and revisit movies they love
    """
    user_id = jwt_service.validate_user_jwt(credentials.credentials)
    # Authentification renforcé au niveau backend en plus de jwt
    if not user_service.is_connected(user_id):
        raise HTTPException(status_code=404, detail="It seem like you are no longer connected.")
    movie = movie_service.get_by_id(movie_id)
    if movie is None:
        raise HTTPException(status_code=404, detail="Movie with this id does not exist.")
    try:
        movie_to_favoritelist = seen_movie_service.add_to_favoritelist(user_id, movie_id)
    except Exception:
        raise HTTPException(status_code=500, detail="Something is going wrong. Try again !") from Exception
    return movie

@watch_movie_route.get("/favorites/get_favorite_list", status_code=status.HTTP_200_OK, dependencies=[Depends(JWTBearer())], summary="Your favorite movies")
def get_favorite_list(credentials: Annotated[HTTPAuthorizationCredentials, Depends(JWTBearer())]):
    """ 
    This action allows you to get your list of movies you have liked as favorite. Authentication is required. A valid token is needed to perform this action and access the watchlist.
    """
    user_id = jwt_service.validate_user_jwt(credentials.credentials)
    # Authentification renforcé au niveau backend en plus de jwt
    if not user_service.is_connected(user_id):
        raise HTTPException(status_code=404, detail="It seem like you are no longer connected.")
    try:
        favoritelist = seen_movie_service.user_favorites_movie(user_id)
    except Exception:
        raise HTTPException(status_code=500, detail="Something is going wrong. Try again !") from Exception
    return seen_movie_service.user_favorites_movie(user_id)

@watch_movie_route.put("/remove-from-user-favorites/{movie_id}", status_code=status.HTTP_200_OK, dependencies=[Depends(JWTBearer())], summary="Remove a movie from your favorites")
def remove_from_user_favorites(movie_id:int, credentials: Annotated[HTTPAuthorizationCredentials, Depends(JWTBearer())]):
    """ 
    This route allows authenticated users to remove a specific movie from their favorites list. A valid token is required to perform this action.
    """
    user_id = jwt_service.validate_user_jwt(credentials.credentials)
    # Authentification renforcé au niveau backend en plus de jwt
    if not user_service.is_connected(user_id):
        raise HTTPException(status_code=404, detail="It seem like you are no longer connected.")
    return seen_movie_service.remote_from_user_favorites(user_id, movie_id)

class RatingMovie(BaseModel):
    movie_id:int
    note: conint(ge=0, le=10) 

@watch_movie_route.post("/note-movie", status_code=status.HTTP_200_OK, dependencies=[Depends(JWTBearer())], summary="Rate a movie")
def note_movie(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(JWTBearer())],
    rating_movie: RatingMovie=Depends(RatingMovie)
    ):
    """ 
    Authenticated users can rate a movie on a scale of 1 to 10. A valid token is required for this operation. If the specified movie ID does not exist, a 404 error will be returned
    """
    user_id = jwt_service.validate_user_jwt(credentials.credentials)
    # Authentification renforcé au niveau backend en plus de jwt
    if not user_service.is_connected(user_id):
        raise HTTPException(status_code=404, detail="It seem like you are no longer connected.")
    movie = movie_service.get_by_id(rating_movie.movie_id)
    if movie is None:
        raise HTTPException(status_code=404, detail="Movie with this id does not exist.")
    try:
        movie = note_service.note_movie(user_id, rating_movie.movie_id, rating_movie.note)
    except Exception:
        raise HTTPException(status_code=500, detail="Something is going wrong. Try again !") from Exception
    return movie

@watch_movie_route.put("/remove-movie-note/{movie_id}", status_code=status.HTTP_200_OK, dependencies=[Depends(JWTBearer())], summary="Remove your movie rating")
def remove_note_movie(movie_id:int, credentials: Annotated[HTTPAuthorizationCredentials, Depends(JWTBearer())]):
    """ 
    You can delete your rating for a specific movie. A valid token is required for this action.
    """
    user_id = jwt_service.validate_user_jwt(credentials.credentials)
    # Authentification renforcé au niveau backend en plus de jwt
    if not user_service.is_connected(user_id):
        raise HTTPException(status_code=404, detail="It seem like you are no longer connected.")
    movie = note_service.remove_note_movie(user_id, movie_id)
    if not movie :
        raise HTTPException(status_code=404, detail="Movie with this id does not exist.")
    else:
        return movie
