from fastapi import APIRouter, HTTPException
from db import database
from model.proveedor import Proveedor, ProveedorCreate, ProveedorInDB

router = APIRouter()

@router.post("/proveedores/", response_model=ProveedorInDB)
async def crear_proveedor(proveedor: ProveedorCreate):
    # Verificar si el proveedor_id ya existe
    query = Proveedor.select().where(Proveedor.c.proveedor_id == proveedor.proveedor_id)
    existing_proveedor = await database.fetch_one(query)

    if existing_proveedor:
        raise HTTPException(status_code=400, detail="El ID del proveedor ya existe")

    # Insertar el nuevo proveedor
    query = Proveedor.insert().values(
        proveedor_id=proveedor.proveedor_id,  # Usar el ID proporcionado
        proveedor_nombre=proveedor.proveedor_nombre,
        proveedor_direccion=proveedor.proveedor_direccion,
        proveedor_telefono=proveedor.proveedor_telefono,
        proveedor_correo=proveedor.proveedor_correo,
        proveedor_status=proveedor.proveedor_status
    )

    try:
        await database.execute(query)
        return {**proveedor.dict()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear el proveedor: {str(e)}")

@router.get("/proveedores/{proveedor_id}", response_model=ProveedorInDB)
async def leer_proveedor(proveedor_id: int):
    query = Proveedor.select().where(Proveedor.c.proveedor_id == proveedor_id)
    proveedor = await database.fetch_one(query)
    if proveedor is None:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")
    return proveedor

@router.get("/proveedores/", response_model=list[ProveedorInDB])
async def leer_proveedores():
    query = Proveedor.select()
    proveedores = await database.fetch_all(query)
    return proveedores

@router.put("/proveedores/{proveedor_id}", response_model=ProveedorInDB)
async def actualizar_proveedor(proveedor_id: int, proveedor: ProveedorCreate):
    query = Proveedor.update().where(Proveedor.c.proveedor_id == proveedor_id).values(**proveedor.dict())
    await database.execute(query)
    return await database.fetch_one(Proveedor.select().where(Proveedor.c.proveedor_id == proveedor_id))

@router.delete("/proveedores/{proveedor_id}")
async def eliminar_proveedor(proveedor_id: int):
    query = Proveedor.select().where(Proveedor.c.proveedor_id == proveedor_id)
    db_proveedor = await database.fetch_one(query)
    if db_proveedor is None:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")
    await database.execute(Proveedor.delete().where(Proveedor.c.proveedor_id == proveedor_id))
    return {"detail": "Proveedor eliminado"}
