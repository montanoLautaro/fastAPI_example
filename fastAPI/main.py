'''
Inicia el server: uvicorn main:app --reload
detener el server: CTRL + C

Documentacion con swagger:  http://127.0.0.1:8000/docs
Documentacion con redoc:  http://127.0.0.1:8000/redoc
'''

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return "hola soy un servidor"
