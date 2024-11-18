from pydantic import BaseModel, conint
from fastapi import APIRouter, Depends, HTTPException, status, Body
from typing import TYPE_CHECKING, Annotated
from fastapi.security import HTTPAuthorizationCredentials
from .JWTBearer import JWTBearer
from .init_app import jwt_service, following_service
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
    return following_service.get_new_follow_suggestion(user_id)