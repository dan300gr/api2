from fastapi import APIRouter, HTTPException
from db import database
from model.inventario import Inventario, InventarioCreate, InventarioInDB

router = APIRouter()

@router.post("/inventarios/", response_model=InventarioInDB)
async def crear_inventario(inventario: InventarioCreate):
    # Verificar si el inventario_id ya existe
    query = Inventario.select().where(Inventario.c.inventario_id == inventario.inventario_id)
    existing_inventario = await database.fetch_one(query)

    if existing_inventario:
        raise HTTPException(status_code=400, detail="El ID del inventario ya existe")

    # Insertar el nuevo inventario
    query = Inventario.insert().values(
        inventario_id=inventario.inventario_id,  # Usar el ID proporcionado
        ubicacion_id=inventario.ubicacion_id,
        producto_id=inventario.producto_id,
        stock_id=inventario.stock_id,
        inventario_cantidad=inventario.inventario_cantidad,
        inventario_status=inventario.inventario_status
    )

    try:
        await database.execute(query)
        return {**inventario.dict()}  # Devuelve el inventario creado
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear el inventario: {str(e)}")

@router.get("/inventarios/{inventario_id}", response_model=InventarioInDB)
async def leer_inventario(inventario_id: int):
    query = Inventario.select().where(Inventario.c.inventario_id == inventario_id)
    inventario = await database.fetch_one(query)
    if inventario is None:
        raise HTTPException(status_code=404, detail="Inventario no encontrado")
    return inventario

@router.get("/inventarios/", response_model=list[InventarioInDB])
async def leer_inventarios():
    query = Inventario.select()
    inventarios = await database.fetch_all(query)
    return inventarios

@router.put("/inventarios/{inventario_id}", response_model=InventarioInDB)
async def actualizar_inventario(inventario_id: int, inventario: InventarioCreate):
    query = Inventario.update().where(Inventario.c.inventario_id == inventario_id).values(**inventario.dict())
    await database.execute(query)
    return await database.fetch_one(Inventario.select().where(Inventario.c.inventario_id == inventario_id))

@router.delete("/inventarios/{inventario_id}")
async def eliminar_inventario(inventario_id: int):
    query = Inventario.select().where(Inventario.c.inventario_id == inventario_id)
    db_inventario = await database.fetch_one(query)
    if db_inventario is None:
        raise HTTPException(status_code=404, detail="Inventario no encontrado")
    await database.execute(Inventario.delete().where(Inventario.c.inventario_id == inventario_id))
    return {"detail": "Inventario eliminado"}
