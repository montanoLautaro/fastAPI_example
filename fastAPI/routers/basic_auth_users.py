from pydantic import BaseModel
# Dependes = la operacion recibe datos, pero no depende de nadie
from fastapi import APIRouter, Depends, HTTPException, status
# AUTENTICACION OAuth2
# request form = forma en la que se envia al backend el usuario y contraseña
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


# uvicorn basic_auth_users:app --reload
router = APIRouter()


# bearer = se encarga de gestionar la autenticacion, usuario y contraseña
# tokenUrl= le damos nombre a la url de auth
oauth2 = OAuth2PasswordBearer(tokenUrl=("login"))


class User(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool


class UserDB(User):
    password: str


# despues reemplazar por una base de datos de verdad
users_db = {
    "nahue": {
        "username": "nahue",
        "full_name": "Montaño Luataro",
        "email": "braismoure@mourede.com",
        "disabled": False,
        "password": "123456"
    },
    "mouredev2": {
        "username": "mouredev2",
        "full_name": "Brais Moure 2",
        "email": "braismoure2@mourede.com",
        "disabled": True,
        "password": "654321"
    }
}


def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])


def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])


# GENERAR EL TOKEN DE AUTENTICACION
@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="El usuario no es correcto")

    user = search_user_db(form.username)
    if not form.password == user.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="La contraseña no es correcta")

    return {"access_token": user.username, "token_type": "bearer"}


# CRITERIO DE DEPENDENCIA
async def current_user(token: str = Depends(oauth2)):
    user = search_user(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales de autenticación inválidas",
            headers={"WWW-Authenticate": "Bearer"})

    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario inactivo")

    return user


# Depends(current_user) = si current_user no retorna un usuario no se ejecuta el codigo de la funcion
@router.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user
