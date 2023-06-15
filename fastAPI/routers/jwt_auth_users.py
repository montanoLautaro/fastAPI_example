"""
Para agregar jwt al proyecto hay que instalar: 

pip install "python-jose[cryptography]"

pip install "passlib[bcrypt]"

libreria que genera el SECRET (devuelve un numero random de 32 en hexadecimal) = openssl rand -hex 32
"""
# uvicorn jwt_auth_users:app --reload

from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta

router = APIRouter()
oauth2 = OAuth2PasswordBearer(tokenUrl=("login"))

# ALGORITMO DE JTW (HS256 es el mas utilizado)
ALGORITHM = "HS256"
ACCES_TOKEN_DURATION = 1
# CLAVE PROPIA que solo el backend conoce
SECRET = "eOj?0NH0<AFTaL-JX2{="

# Algoritmo de encriptacion
crypt = CryptContext(schemes=["bcrypt"])


class User(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool


class UserDB(User):
    password: str


users_db = {
    "nahue": {
        "username": "nahue",
        "full_name": "Montaño Luataro",
        "email": "braismoure@mourede.com",
        "disabled": False,
        "password": "$2a$12$vUWM8OKxCVb5mxKByrYHuuK6OSxBla6JBzpcdcExq31oc3k95Lcvq"
    },
    "mouredev2": {
        "username": "mouredev2",
        "full_name": "Brais Moure 2",
        "email": "braismoure2@mourede.com",
        "disabled": True,
        "password": "$2a$12$tmwov365/E1JBJaNXIVNdeTGoIkS3536iPHTUCyzn2wLvLo8A4Ome"
    }
}


def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])


@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="El usuario no es correcto")

    user = search_user_db(form.username)

    # VERIFICAMOS si la contraseña esta encriptada

    if not crypt.verify(form.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="La contraseña no es correcta")

    # DURACION del token en minutos
    acces_token_expiration = timedelta(minutes=ACCES_TOKEN_DURATION)

    # EXPIRACION del token, hora actual + duracion
    expire = datetime.utcnow() + acces_token_expiration

    # sub = nombreUsuario, exp = tiempo de exp
    acces_token = {"sub": user.username,
                   "exp": expire}

    # encode codifica el token
    return {"access_token": jwt.encode(acces_token, SECRET, algorithm=ALGORITHM), "token_type": "bearer"}


def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])


async def auth_user(token: str = Depends(oauth2)):
    exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciales de autenticación inválidas",
        headers={"WWW-Authenticate": "Bearer"})

    try:
        # decode descodifica el token para recibir los datos del usuario, ej nombre del usuario
        username = jwt.decode(token, SECRET, algorithms=ALGORITHM).get("sub")

        if username is None:
            raise exception

        return search_user(username)

    except JWTError:
        raise exception


async def current_user(user: User = Depends(auth_user)):
    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario inactivo")

    return user


@router.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user
