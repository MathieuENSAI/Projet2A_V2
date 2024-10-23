from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
import secrets
import jwt
from datetime import datetime, timedelta
import os

# Clé secrète pour signer les tokens JWT
SECRET_KEY = secrets.token_urlsafe(32)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
SERVER_VALIDE_TOKENS = {}

# OAuth2PasswordBearer est utilisé pour extraire le token de l'en-tête "Authorization"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="connexion")

# Modèle pour représenter un token
class TokenModel(BaseModel):
    access_token: str
    token_type: str = "bearer"

# Fonction pour créer un token JWT
def creer_token(username:str, secret_key:str= SECRET_KEY):
    payload = {
        "sub": username,
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    }
    encoded_jwt = jwt.encode(payload, secret_key, algorithm=ALGORITHM)
    return encoded_jwt

# Fonction pour vérifier le token JWT
def verifier_token(token: str = Depends(oauth2_scheme), secret_key: str = SECRET_KEY):
    try:
        payload = jwt.decode(token, secret_key, algorithms=[ALGORITHM])
        pseudo: str = payload.get("sub")
        if pseudo in SERVER_VALIDE_TOKENS and SERVER_VALIDE_TOKENS[pseudo] == token:
            return pseudo
        else:
            raise HTTPException(status_code=401, detail="Token invalide")
       
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Token invalide ou expiré")