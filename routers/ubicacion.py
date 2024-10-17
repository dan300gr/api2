from fastapi import APIRouter, HTTPException
from db import database
from model.ubicacion import Ubicacion, UbicacionCreate, UbicacionInDB

router = APIRouter()

@router.post("/ubicaciones/", response_model=UbicacionInDB)
async def crear_ubicacion(ubicacion: UbicacionCreate):
    # Verificar si el ubicacion_id ya existe
    query = Ubicacion.select().where(Ubicacion.c.ubicacion_id == ubicacion.ubicacion_id)
    existing_ubicacion = await database.fetch_one(query)

    if existing_ubicacion:
        raise HTTPException(status_code=400, detail="El ID de la ubicación ya existe")

    # Insertar la nueva ubicación
    query = Ubicacion.insert().values(
        ubicacion_id=ubicacion.ubicacion_id,  # Usar el ID proporcionado
        ubicacion_nombre=ubicacion.ubicacion_nombre,
        edificio_id=ubicacion.edificio_id,  # Aquí se usa el campo correcto
        ubicacion_status=ubicacion.ubicacion_status
    )

    try:
        await database.execute(query)
        return {**ubicacion.dict()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear la ubicación: {str(e)}")

@router.get("/ubicaciones/{ubicacion_id}", response_model=UbicacionInDB)
async def leer_ubicacion(ubicacion_id: int):
    query = Ubicacion.select().where(Ubicacion.c.ubicacion_id == ubicacion_id)
    ubicacion = await database.fetch_one(query)
    if ubicacion is None:
        raise HTTPException(status_code=404, detail="Ubicación no encontrada")
    return ubicacion

@router.get("/ubicaciones/", response_model=list[UbicacionInDB])
async def leer_ubicaciones():
    query = Ubicacion.select()
    ubicaciones = await database.fetch_all(query)
    return ubicaciones

@router.put("/ubicaciones/{ubicacion_id}", response_model=UbicacionInDB)
async def actualizar_ubicacion(ubicacion_id: int, ubicacion: UbicacionCreate):
    query = Ubicacion.update().where(Ubicacion.c.ubicacion_id == ubicacion_id).values(**ubicacion.dict())
    await database.execute(query)
    return await database.fetch_one(Ubicacion.select().where(Ubicacion.c.ubicacion_id == ubicacion_id))

@router.delete("/ubicaciones/{ubicacion_id}")
async def eliminar_ubicacion(ubicacion_id: int):
    query = Ubicacion.select().where(Ubicacion.c.ubicacion_id == ubicacion_id)
    db_ubicacion = await database.fetch_one(query)
    if db_ubicacion is None:
        raise HTTPException(status_code=404, detail="Ubicación no encontrada")
    await database.execute(Ubicacion.delete().where(Ubicacion.c.ubicacion_id == ubicacion_id))
    return {"detail": "Ubicación eliminada"}

