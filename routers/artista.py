from fastapi import APIRouter, HTTPException
from db import database
from model.artista import Artista, ArtistaCreate, ArtistaInDB

router = APIRouter()

@router.post("/artistas/", response_model=ArtistaInDB)
async def crear_artista(artista: ArtistaCreate):
    # Verificar si el artista_id ya existe
    query = Artista.select().where(Artista.c.artista_id == artista.artista_id)
    existing_artista = await database.fetch_one(query)

    if existing_artista:
        raise HTTPException(status_code=400, detail="El ID del artista ya existe")

    # Insertar el nuevo artista
    query = Artista.insert().values(
        artista_id=artista.artista_id,  # Usar el ID proporcionado
        artista_nombre=artista.artista_nombre,
        artista_status=artista.artista_status
    )

    try:
        await database.execute(query)
        return {**artista.dict()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear el artista: {str(e)}")

@router.get("/artistas/{artista_id}", response_model=ArtistaInDB)
async def leer_artista(artista_id: int):
    query = Artista.select().where(Artista.c.artista_id == artista_id)
    artista = await database.fetch_one(query)
    if artista is None:
        raise HTTPException(status_code=404, detail="Artista no encontrado")
    return artista

@router.get("/artistas/", response_model=list[ArtistaInDB])
async def leer_artistas():
    query = Artista.select()
    artistas = await database.fetch_all(query)
    return artistas

@router.put("/artistas/{artista_id}", response_model=ArtistaInDB)
async def actualizar_artista(artista_id: int, artista: ArtistaCreate):
    query = Artista.update().where(Artista.c.artista_id == artista_id).values(**artista.dict())
    await database.execute(query)
    return await database.fetch_one(Artista.select().where(Artista.c.artista_id == artista_id))

@router.delete("/artistas/{artista_id}")
async def eliminar_artista(artista_id: int):
    query = Artista.select().where(Artista.c.artista_id == artista_id)
    db_artista = await database.fetch_one(query)
    if db_artista is None:
        raise HTTPException(status_code=404, detail="Artista no encontrado")
    await database.execute(Artista.delete().where(Artista.c.artista_id == artista_id))
    return {"detail": "Artista eliminado"}
