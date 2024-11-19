from pydantic import BaseModel, conint
from fastapi import APIRouter, Depends, HTTPException, status, Body
from typing import TYPE_CHECKING, Annotated
from fastapi.security import HTTPAuthorizationCredentials
from .JWTBearer import JWTBearer
from .init_app import jwt_service, following_service
import logging

following_route = APIRouter(prefix="/follow", tags=["User Following"])

@following_route.post("/", status_code=status.HTTP_200_OK, dependencies=[Depends(JWTBearer())], summary="Add a new following")
def add_following(following_id: int, credentials: Annotated[HTTPAuthorizationCredentials, Depends(JWTBearer())]):
    """
    Add a user to your followings list
    """
    user_id = jwt_service.validate_user_jwt(credentials.credentials)
    if user_id == following_id:
        return None
    following = following_service.add_following(user_id, following_id)
    if following is None:
        raise HTTPException(status_code=404, detail=f"You can not follow user with id[{following_id}]. check and try adain")
    return {"following":following} |following_service.get_following_movies_collection(user_id, following_id)

@following_route.delete("/stop-follow/{following_id}",  status_code=status.HTTP_200_OK, dependencies=[Depends(JWTBearer())], summary= "Stop following a user")
def stop_follow(following_id: int, credentials: Annotated[HTTPAuthorizationCredentials, Depends(JWTBearer())]):
    
    """
    Stop following this user
    """
    user_id = jwt_service.validate_user_jwt(credentials.credentials)
    return following_service.stop_follow(user_id, following_id)

@following_route.get("/all-followings",  status_code=status.HTTP_200_OK, dependencies=[Depends(JWTBearer())], summary="Your followings")
def all_following(credentials: Annotated[HTTPAuthorizationCredentials, Depends(JWTBearer())]):
    """ 
    Your followings
    """
    user_id = jwt_service.validate_user_jwt(credentials.credentials)
    return following_service.get_all_following(user_id)

@following_route.get("/following-movies-collection/{following_id}",  status_code=status.HTTP_200_OK, dependencies=[Depends(JWTBearer())])
def get_following_movies_collection(following_id: int, credentials: Annotated[HTTPAuthorizationCredentials, Depends(JWTBearer())]):
    """ 
    Get this following movies collection
    """
    user_id = jwt_service.validate_user_jwt(credentials.credentials)
    if following_service.is_user_follow(user_id, following_id):
        return following_service.get_following_movies_collection(user_id, following_id)
    else:
       raise HTTPException(status_code=404, detail=f"You can not get movies collections from this user.")
