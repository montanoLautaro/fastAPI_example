# operaciones para el modelo user de mongodb (service)
# Parseo de lo que viene en bd al modelo User
def user_schema(user) -> dict:
    return {
        "id": str(user["_id"]),
        "username": str(user["username"]),
        "email": str(user["email"])
    }

# Parsea a cada elemento de la lista, del usuario de bd al modelo de User


def users_schema(users) -> list:
    return [user_schema(user) for user in users]
