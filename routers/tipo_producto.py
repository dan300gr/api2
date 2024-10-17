from fastapi import APIRouter, HTTPException
from db import database
from model.tipo_producto import TipoProducto, TipoProductoCreate, TipoProductoInDB

router = APIRouter()

@router.post("/tipos-producto/", response_model=TipoProductoInDB)
async def crear_tipo_producto(tipo_producto: TipoProductoCreate):
    # Verificar si el tipo_id ya existe
    query = TipoProducto.select().where(TipoProducto.c.tipo_id == tipo_producto.tipo_id)
    existing_tipo = await database.fetch_one(query)

    if existing_tipo:
        raise HTTPException(status_code=400, detail="El ID del tipo de producto ya existe")

    # Insertar el nuevo tipo de producto
    query = TipoProducto.insert().values(
        tipo_id=tipo_producto.tipo_id,  # Usar el ID proporcionado
        tipo_nombre=tipo_producto.tipo_nombre,
        tipo_status=tipo_producto.tipo_status
    )

    try:
        await database.execute(query)
        return {**tipo_producto.dict()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear el tipo de producto: {str(e)}")

@router.get("/tipos-producto/{tipo_id}", response_model=TipoProductoInDB)
async def leer_tipo_producto(tipo_id: int):
    query = TipoProducto.select().where(TipoProducto.c.tipo_id == tipo_id)
    tipo_producto = await database.fetch_one(query)
    if tipo_producto is None:
        raise HTTPException(status_code=404, detail="Tipo de producto no encontrado")
    return tipo_producto

@router.get("/tipos-producto/", response_model=list[TipoProductoInDB])
async def leer_tipos_producto():
    query = TipoProducto.select()
    tipos_producto = await database.fetch_all(query)
    return tipos_producto

@router.put("/tipos-producto/{tipo_id}", response_model=TipoProductoInDB)
async def actualizar_tipo_producto(tipo_id: int, tipo_producto: TipoProductoCreate):
    query = TipoProducto.update().where(TipoProducto.c.tipo_id == tipo_id).values(**tipo_producto.dict())
    await database.execute(query)
    return await database.fetch_one(TipoProducto.select().where(TipoProducto.c.tipo_id == tipo_id))

@router.delete("/tipos-producto/{tipo_id}")
async def eliminar_tipo_producto(tipo_id: int):
    query = TipoProducto.select().where(TipoProducto.c.tipo_id == tipo_id)
    db_tipo_producto = await database.fetch_one(query)
    if db_tipo_producto is None:
        raise HTTPException(status_code=404, detail="Tipo de producto no encontrado")
    await database.execute(TipoProducto.delete().where(TipoProducto.c.tipo_id == tipo_id))
    return {"detail": "Tipo de producto eliminado"}
