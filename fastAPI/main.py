'''
Inicia el server: uvicorn main:app --reload
detener el server: CTRL + C

Documentacion con swagger:  http://127.0.0.1:8000/docs
Documentacion con redoc:  http://127.0.0.1:8000/redoc

instalar modulo mongodb: pip install pymongo
'''
from fastapi import FastAPI
from routers import users, users_db, products, jwt_auth_users
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# IMPORTANTE AGREGAR ROUTERS, para que corran los url de los archivos que estan dentro de router
# app.include_router(users.router)
# app.include_router(basic_auth_users.router)
app.include_router(products.router)
app.include_router(users_db.router)
app.include_router(jwt_auth_users.router)

# Recursos estaticos
# url que le asigno, directorio y nombre que le doy al archivo
app.mount("/static", StaticFiles(directory="static"), name="Elden Ring")


@app.get("/")
async def root():
    return "hola soy un servidor"
