from pydantic import BaseModel, conint
from fastapi import APIRouter, Depends, HTTPException, status, Body
from typing import TYPE_CHECKING, Annotated
from fastapi.security import HTTPAuthorizationCredentials
from .JWTBearer import JWTBearer
from .init_app import jwt_service, user_service, following_service, user_service
import logging

following_route = APIRouter(prefix="/follow", tags=["User Following"])

@following_route.post("/id", status_code=status.HTTP_200_OK, dependencies=[Depends(JWTBearer())], summary="Add a new following")
def add_following(following_id: int, credentials: Annotated[HTTPAuthorizationCredentials, Depends(JWTBearer())]):
    """
    This action allows you to add a user to your following list, enabling you to receive updates and recommendations based on their activity. A valid authentication token is required.
    """
    user_id = jwt_service.validate_user_jwt(credentials.credentials)
    if user_id == following_id:
        return None
    # Authentification renforcé au niveau backend en plus de jwt
    if not user_service.is_connected(user_id):
        raise HTTPException(status_code=404, detail="It seem like you are no longer connected.")
    following = following_service.add_following(user_id, following_id)
    if following is None:
        raise HTTPException(status_code=404, detail=f"You can not follow user with id[{following_id}]. check and try again")
    return {"following":following} |following_service.get_following_movies_collection(user_id, following_id)

@following_route.post("/username", status_code=status.HTTP_200_OK, dependencies=[Depends(JWTBearer())], summary="Add a new following by username")
def add_following_by_username(username: str, credentials: Annotated[HTTPAuthorizationCredentials, Depends(JWTBearer())]):
    """
    This action allows you to add a user to your following list, enabling you to receive updates and recommendations based on their activity. A valid authentication token is required.
    """
    user_id = jwt_service.validate_user_jwt(credentials.credentials)
    # Authentification renforcé au niveau backend en plus de jwt
    if not user_service.is_connected(user_id):
        raise HTTPException(status_code=404, detail="It seem like you are no longer connected.")
    following = user_service.get_user_by_username(username=username)
    if following is None :
        raise HTTPException(status_code=404, detail=f"User with this username[{username}] doesn't not exist. check and try again")
    following_id = following.id_user
    if user_id == following_id:
        return None
    following = following_service.add_following(user_id, following_id)
    return {"following":following} |following_service.get_following_movies_collection(user_id, following_id)

@following_route.delete("/stop-follow/id/{following_id}",  status_code=status.HTTP_200_OK, dependencies=[Depends(JWTBearer())], summary= "Stop following a user")
def stop_follow(following_id: int, credentials: Annotated[HTTPAuthorizationCredentials, Depends(JWTBearer())]):
    
    """
    Unfollow a user. Once you stop following, you will no longer receive their updates or suggestions. Please note that authentication is required for this operation.
    """
    user_id = jwt_service.validate_user_jwt(credentials.credentials)
    # Authentification renforcé au niveau backend en plus de jwt
    if not user_service.is_connected(user_id):
        raise HTTPException(status_code=404, detail="It seem like you are no longer connected.")
    return following_service.stop_follow(user_id, following_id)

@following_route.delete("/stop-follow/username/{username}",  status_code=status.HTTP_200_OK, dependencies=[Depends(JWTBearer())], summary= "Stop following a user")
def stop_follow(username: str, credentials: Annotated[HTTPAuthorizationCredentials, Depends(JWTBearer())]):
    
    """
    Unfollow a user. Once you stop following, you will no longer receive their updates or suggestions. Please note that authentication is required for this operation.
    """
    user_id = jwt_service.validate_user_jwt(credentials.credentials)
    # Authentification renforcé au niveau backend en plus de jwt
    if not user_service.is_connected(user_id):
        raise HTTPException(status_code=404, detail="It seem like you are no longer connected.")
    following = user_service.get_user_by_username(username=username)
    if following is None :
        raise HTTPException(status_code=404, detail=f"User with this username[{username}] doesn't not exist. check and try again")
    following_id = following.id_user
    return following_service.stop_follow(user_id, following_id)

@following_route.get("/all-followings",  status_code=status.HTTP_200_OK, dependencies=[Depends(JWTBearer())], summary="View all users you are following")
def all_following(credentials: Annotated[HTTPAuthorizationCredentials, Depends(JWTBearer())]):
    """ 
    Retrieve a list of all users you are currently following. Authentication is required for access.
    """
    user_id = jwt_service.validate_user_jwt(credentials.credentials)
    # Authentification renforcé au niveau backend en plus de jwt
    if not user_service.is_connected(user_id):
        raise HTTPException(status_code=404, detail="It seem like you are no longer connected.")
    return following_service.get_all_following(user_id)

@following_route.get("/following-movies-collection/{following_id}",  status_code=status.HTTP_200_OK, dependencies=[Depends(JWTBearer())], summary="Retrieve the movie collection of a followed use")
def get_following_movies_collection(following_id: int, credentials: Annotated[HTTPAuthorizationCredentials, Depends(JWTBearer())]):
    """ 
    This action provides two key pieces of information: a list of movies the user you're following has seen and a collection of movies that both you and the followed user have seen together. Access is granted only if you're following the user, and a valid authentication token is required.
    """
    user_id = jwt_service.validate_user_jwt(credentials.credentials)
    # Authentification renforcé au niveau backend en plus de jwt
    if not user_service.is_connected(user_id):
        raise HTTPException(status_code=404, detail="It seem like you are no longer connected.")
    if following_service.is_user_follow(user_id, following_id):
        return following_service.get_following_movies_collection(user_id, following_id)
    else:
       raise HTTPException(status_code=404, detail=f"You can not get movies collections from this user.")
