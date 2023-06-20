### Users DB API ###

from fastapi import APIRouter, HTTPException, status
from database.models.user import User
from database.client import db_client
from database.schemas.user import user_schema, users_schema
from bson import ObjectId


router = APIRouter(prefix="/usersdb",
                   tags=["users"],
                   responses={404: {"message": "No encontrado."}})


@router.post("/", response_model=User, status_code=201)
async def user(user: User):
    if type(search_user_by_email(user.email)) == User:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="El usuario ya existe"
        )

    # transformo al user en un diccionario
    user_dict = dict(user)

    # me aseguro de que se elimine el campo id, ya que se autogenera con mongodb
    del user_dict["id"]

    # guardar usuario en bd, con id autogenerado
    id = db_client.users.insert_one(user_dict).inserted_id

    # Comprobamos si se guardo en bd, el nombre del campo que crea mongodb por defecto es _id
    new_user = user_schema(db_client.users.find_one({"_id": id}))

    print(f"new user {new_user}")

    return User(**new_user)


# findAll
@router.get("/", response_model=list[User])
async def users():
    return users_schema(db_client.users.find())


@router.get("/{id}")  # Path
async def users(id: str):
    return search_user("_id", ObjectId(id))


@router.get("/")
async def user(id: str):  # Query
    return search_user("_id", ObjectId(id))


@router.put("/", response_model=User)
async def update_user(user: User):
    try:
        user_dict = dict(user)
        # elimino el campo id, ya que es algo que no tengo que modificar
        del user_dict["id"]
        db_client.users.find_one_and_replace(
            {"_id": ObjectId(user.id)}, user_dict)
    except:
        return {"Error": "Ha ocurrido un error."}

    return search_user("_id", ObjectId(user.id))


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(id: str):
    found = db_client.users.find_one_and_delete({"_id": ObjectId(id)})

    if not found:
        return {"error": "No se ha eliminado el usuario indicado."}


def search_user_by_email(email: str):
    try:
        user = db_client.users.find_one({"email": email})
        return User(**user_schema(user))
    except:
        return {"Error": "El correo electrónico no es válido."}


def search_user_by_id(id):
    try:
        user = db_client.users.find_one({"_id": id})
        return User(**user_schema(user))
    except:
        return {"Error": "No se ha encontrado el usuario."}


# busqueda generica
def search_user(field: str, key):
    try:
        user = db_client.users.find_one({field: key})
        return User(**user_schema(user))
    except:
        return {"Error": "No se ha encontrado el usuario."}
