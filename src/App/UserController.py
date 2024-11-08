from typing import TYPE_CHECKING, Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials

from src.Model.APIUser import APIUser
from src.Model.JWTResponse import JWTResponse
from src.Service.PasswordService import check_password_strength, validate_username_password

from .init_app import jwt_service, user_repo, user_service
from .JWTBearer import JWTBearer

if TYPE_CHECKING:
    from src.Model.User import User

user_router = APIRouter(prefix="/users", tags=["Users"])


@user_router.post("/singup", status_code=status.HTTP_201_CREATED)
def create_user(username: str, pass_word: str) -> APIUser:
    """
    Performs validation on the username and password
    """
    try:
        check_password_strength(pass_word=pass_word)
    except Exception:
        raise HTTPException(status_code=400, detail="Password too weak") from Exception

    if user_service.user_exists(username):
        raise HTTPException(status_code=409, detail="User with this username already exists")

    user= user_service.create_user(username=username, pass_word=pass_word)
    if user is None:
        raise HTTPException(status_code = 500, detail = "Failed to create a user. Please try again later")

    return APIUser(id=user.id_user, username=user.username)


@user_router.post("/login", status_code=status.HTTP_201_CREATED)
def login(username: str, pass_word: str) -> JWTResponse:
    """
    Authenticate with username and password and obtain a token
    """
    try:
        user = validate_username_password(username=username, pass_word=pass_word, user_repo=user_repo)
    except Exception as error:
        raise HTTPException(status_code=403, detail="Invalid username and password combination") from error

    return jwt_service.encode_jwt(user.id_user)


@user_router.get("/me", dependencies=[Depends(JWTBearer())])
def get_user_own_profile(credentials: Annotated[HTTPAuthorizationCredentials, Depends(JWTBearer())]) -> APIUser:
    """
    Get the authenticated user profile
    """
    return get_user_from_credentials(credentials)


def get_user_from_credentials(credentials: HTTPAuthorizationCredentials) -> APIUser:
    token = credentials.credentials
    user_id = int(jwt_service.validate_user_jwt(token))
    user: User | None = user_repo.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return APIUser(id=user.id_user, username=user.username)
