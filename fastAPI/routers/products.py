from fastapi import APIRouter
"""
 con prefix indicamos que las url de este archivo empiezan con /products
 con tags lo divide en swagger por categoria, products en este caso
"""
router = APIRouter(prefix="/products",
                   tags=["products"],
                   responses={404: {"mensaje": "No encontrado."}})

products_list = ["producto 1", "Producto 2", "Producto 3"]


@router.get("/")
async def get_all_products():
    return products_list


@router.get("/{id}")
async def get_product(id: int):
    return products_list[id]
