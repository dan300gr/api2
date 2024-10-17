from fastapi import APIRouter, HTTPException
from db import database
from model.producto import Producto, ProductoCreate, ProductoInDB

router = APIRouter()

@router.post("/productos/", response_model=ProductoInDB)
async def crear_producto(producto: ProductoCreate):
    # Verificar si el producto_id ya existe
    query = Producto.select().where(Producto.c.producto_id == producto.producto_id)
    existing_product = await database.fetch_one(query)

    if existing_product:
        raise HTTPException(status_code=400, detail="El ID del producto ya existe")

    # Insertar el nuevo producto con el ID proporcionado
    query = Producto.insert().values(
        producto_id=producto.producto_id,  # Usar el ID proporcionado
        producto_nombre=producto.producto_nombre,
        producto_precio=producto.producto_precio,
        tipo_id=producto.tipo_id,
        catalogo_id=producto.catalogo_id,
        album_id=producto.album_id,
        producto_status=producto.producto_status
    )

    try:
        await database.execute(query)
        return {**producto.dict()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear el producto: {str(e)}")


@router.get("/productos/{producto_id}", response_model=ProductoInDB)
async def leer_producto(producto_id: int):
    query = Producto.select().where(Producto.c.producto_id == producto_id)
    producto = await database.fetch_one(query)
    if producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto

@router.get("/productos/", response_model=list[ProductoInDB])
async def leer_productos():
    query = Producto.select()
    productos = await database.fetch_all(query)
    return productos

@router.put("/productos/{producto_id}", response_model=ProductoInDB)
async def actualizar_producto(producto_id: int, producto: ProductoCreate):
    query = Producto.update().where(Producto.c.producto_id == producto_id).values(**producto.dict())
    await database.execute(query)
    return await database.fetch_one(Producto.select().where(Producto.c.producto_id == producto_id))

@router.delete("/productos/{producto_id}")
async def eliminar_producto(producto_id: int):
    query = Producto.select().where(Producto.c.producto_id == producto_id)
    db_producto = await database.fetch_one(query)
    if db_producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    await database.execute(Producto.delete().where(Producto.c.producto_id == producto_id))
    return {"detail": "Producto eliminado"}
