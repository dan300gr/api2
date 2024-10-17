from fastapi import APIRouter, HTTPException
from db import database
from model.edificio import Edificio, EdificioCreate, EdificioInDB

router = APIRouter()

@router.post("/edificios/", response_model=EdificioInDB)
async def crear_edificio(edificio: EdificioCreate):
    # Verificar si el edificio_id ya existe
    query = Edificio.select().where(Edificio.c.edificio_id == edificio.edificio_id)
    existing_edificio = await database.fetch_one(query)

    if existing_edificio:
        raise HTTPException(status_code=400, detail="El ID del edificio ya existe")

    # Insertar el nuevo edificio
    query = Edificio.insert().values(
        edificio_id=edificio.edificio_id,  # Usar el ID proporcionado
        edificio_nombre=edificio.edificio_nombre,
        edificio_direccion=edificio.edificio_direccion,
        edificio_status=edificio.edificio_status
    )

    try:
        await database.execute(query)
        return {**edificio.dict()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear el edificio: {str(e)}")

@router.get("/edificios/{edificio_id}", response_model=EdificioInDB)
async def leer_edificio(edificio_id: int):
    query = Edificio.select().where(Edificio.c.edificio_id == edificio_id)
    edificio = await database.fetch_one(query)
    if edificio is None:
        raise HTTPException(status_code=404, detail="Edificio no encontrado")
    return edificio

@router.get("/edificios/", response_model=list[EdificioInDB])
async def leer_edificios():
    query = Edificio.select()
    edificios = await database.fetch_all(query)
    return edificios

@router.put("/edificios/{edificio_id}", response_model=EdificioInDB)
async def actualizar_edificio(edificio_id: int, edificio: EdificioCreate):
    query = Edificio.update().where(Edificio.c.edificio_id == edificio_id).values(**edificio.dict())
    await database.execute(query)
    return await database.fetch_one(Edificio.select().where(Edificio.c.edificio_id == edificio_id))

@router.delete("/edificios/{edificio_id}")
async def eliminar_edificio(edificio_id: int):
    query = Edificio.select().where(Edificio.c.edificio_id == edificio_id)
    db_edificio = await database.fetch_one(query)
    if db_edificio is None:
        raise HTTPException(status_code=404, detail="Edificio no encontrado")
    await database.execute(Edificio.delete().where(Edificio.c.edificio_id == edificio_id))
    return {"detail": "Edificio eliminado"}
