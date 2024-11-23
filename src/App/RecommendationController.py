from pydantic import BaseModel, conint
from fastapi import APIRouter, Depends, HTTPException, status, Body
from typing import TYPE_CHECKING, Annotated
from fastapi.security import HTTPAuthorizationCredentials
from .JWTBearer import JWTBearer
from .init_app import jwt_service, user_service, following_service, seen_movie_service
import logging

recommendation_route = APIRouter(prefix="/recommendation", tags=["Recommendations"])

@recommendation_route.get("/new-following-suggestion", 
                        status_code=status.HTTP_200_OK, dependencies=[Depends(JWTBearer())],
                        summary="New following suggestion")
async def new_follow_suggestion(credentials: Annotated[HTTPAuthorizationCredentials, Depends(JWTBearer())]):
    """
    You have new following suggestion.
    """
    user_id = jwt_service.validate_user_jwt(credentials.credentials)
    # Authentification renforcé au niveau backend en plus de jwt
    if not user_service.is_connected(user_id):
        raise HTTPException(status_code=404, detail="It seem like you are no longer connected.")
    return following_service.get_new_follow_suggestion(user_id)


@recommendation_route.get("/movies-liked-by-your-followings",
                        status_code=status.HTTP_200_OK, dependencies=[Depends(JWTBearer())],
                        summary="Your followings liked these movies")
async def movies_likes_by_followings(credentials: Annotated[HTTPAuthorizationCredentials, Depends(JWTBearer())]):
    """
    Discover these movies—your followings have enjoyed them, and you haven't seen them yet!
    """
    user_id = jwt_service.validate_user_jwt(credentials.credentials)
    # Authentification renforcé au niveau backend en plus de jwt
    if not user_service.is_connected(user_id):
        raise HTTPException(status_code=404, detail="It seem like you are no longer connected.")
    return following_service.get_movies_liked_by_followings(user_id)


@recommendation_route.get("/movies-seen-by-your-followings",
                        status_code=status.HTTP_200_OK, dependencies=[Depends(JWTBearer())],
                        summary="Your followings watched these movies")
async def movies_likes_by_followings(credentials: Annotated[HTTPAuthorizationCredentials, Depends(JWTBearer())]):
    """
    Check out these movies—your followings have watched them, but you haven't yet!
    """
    user_id = jwt_service.validate_user_jwt(credentials.credentials)
    # Authentification renforcé au niveau backend en plus de jwt
    if not user_service.is_connected(user_id):
        raise HTTPException(status_code=404, detail="It seem like you are no longer connected.")
    return following_service.get_movies_seen_by_followings(user_id)


@recommendation_route.get("/others-users-liked-these-movies",
                        status_code=status.HTTP_200_OK, dependencies=[Depends(JWTBearer())],
                        summary="Others users liked these movies")
async def top_movies_liked_by_others_users(credentials: Annotated[HTTPAuthorizationCredentials, Depends(JWTBearer())]):
    """
    Other users liked these movies that you haven't watched yet!
    """
    user_id = jwt_service.validate_user_jwt(credentials.credentials)
    # Authentification renforcé au niveau backend en plus de jwt
    if not user_service.is_connected(user_id):
        raise HTTPException(status_code=404, detail="It seem like you are no longer connected.")
    return seen_movie_service.get_top_movies_liked_by_others_users(user_id)