### Users DB API ###

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel


router = APIRouter(prefix="/users_db",
                   tags=["users"],
                   responses={404: {"message": "No encontrado."}})


@router.get("/")
async def users():
    return  # users_db


@router.get("/{id}")  # Path
async def users(id: int):
    return  # users_db


@router.get("/")
async def user(id: int):
    return  # user


@router.post("/", response_model=User, status_code=201)
async def user(user: User):
    if type("""useR""") == User:
        raise HTTPException(status_code=404, detail="El usuario ya existe.")
    # user.append
    return user


@router.put("/")
async def update_user(user: User):
    for index, user_saved in enumerate(users_list):
        if user_saved.id == user.id:
            users_list[index] = user
            return {"Mensaje": "Operación realizada con éxito."}
    else:
        return {"Error": "Ha ocurrido un error."}


@router.delete("/{id}")
async def delete_user(id: int):
    for index, user_saved in enumerate(users_list):
        if user_saved.id == id:
            del users_list[index]
            return {"Mensaje": "Operación realizada con éxito."}
    else:
        return {"Error": "El usuario que desea eliminar no existe."}
