from pydantic import BaseModel
from fastapi import FastAPI


app = FastAPI()

# Inicia el server: uvicorn users:app --reload


@app.get("/users")
async def users():
    return "hola soy un servidor"


class User(BaseModel):
    name: str
    surname: str
    url: str
    age: int
