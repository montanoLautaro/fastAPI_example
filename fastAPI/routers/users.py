### Users de prueba sin db ###

# Inicia el server al inicializar el main ya que es un router
from pydantic import BaseModel
from fastapi import APIRouter, HTTPException

router = APIRouter()

# BaseModel hace que sea interpretado como un json automaticamente


class User(BaseModel):
    id: int
    name: str
    surname: str
    url: str
    age: int


users_list = [User(id=1, name="Lautaro", surname="Montaño",
              url="https://www.linkedin.com/in/montanolautaro/", age=26),
              User(id=2, name="Juan", surname="Pere",
              url="https://www.google.com", age=33)]


@router.get("/users")
async def all_users():
    return users_list


# DOS TIPOS DE PETICIONES = Path y query

# Path se suele utilizar para datos obligatorios como un id
@router.get("/user/{id}")
async def user(id: int):
    return search_user_by_id(id)


# Query
# ej: http://127.0.0.1:8000/user/?id=2
@router.get("/user/")
async def user(id: int):
    return search_user_by_id(id)


def search_user_by_id(id: int):
    users = filter(lambda user: user.id == id, users_list)
    try:
        return list(users)[0]
    except:
        return {"Error": "No se ha encontrado el usuario."}


# status_code = es el estado que devuelve la petición, si no se modifica devuelve un 200 ok o un 400 en el caso de error
@router.post("/user/")
async def create_user(user: User):
    try:
        if type(search_user_by_id(user.id)) == User:
            return {"Error": "El usuario ya existe."}

        users_list.append(user)
        return user
    except:
        raise HTTPException(status_code=400, detail="Ha ocurrido un error.")


@router.put("/user/")
async def update_user(user: User):
    for index, user_saved in enumerate(users_list):
        if user_saved.id == user.id:
            users_list[index] = user
            return {"Mensaje": "Operación realizada con éxito."}
    else:
        return {"Error": "Ha ocurrido un error."}


@router.delete("/user/{id}")
async def delete_user(id: int):
    for index, user_saved in enumerate(users_list):
        if user_saved.id == id:
            del users_list[index]
            return {"Mensaje": "Operación realizada con éxito."}
    else:
        return {"Error": "El usuario que desea eliminar no existe."}
