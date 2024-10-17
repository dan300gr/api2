from fastapi import APIRouter, HTTPException
from db import database
from model.catalogo import Catalogo, CatalogoCreate, CatalogoInDB

router = APIRouter()

@router.post("/catalogos/", response_model=CatalogoInDB)
async def crear_catalogo(catalogo: CatalogoCreate):
    # Verificar si el catalogo_id ya existe
    query = Catalogo.select().where(Catalogo.c.catalogo_id == catalogo.catalogo_id)
    existing_catalogo = await database.fetch_one(query)

    if existing_catalogo:
        raise HTTPException(status_code=400, detail="El ID del catálogo ya existe")

    # Insertar el nuevo catálogo
    query = Catalogo.insert().values(
        catalogo_id=catalogo.catalogo_id,  # Usar el ID proporcionado
        catalogo_nombre=catalogo.catalogo_nombre,
        catalogo_status=catalogo.catalogo_status
    )

    try:
        await database.execute(query)
        return {**catalogo.dict()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear el catálogo: {str(e)}")


@router.get("/catalogos/", response_model=list[CatalogoInDB])
async def leer_catalogos():
    query = Catalogo.select()
    catalogos = await database.fetch_all(query)
    return catalogos

@router.put("/catalogos/{catalogo_id}", response_model=CatalogoInDB)
async def actualizar_catalogo(catalogo_id: int, catalogo: CatalogoCreate):
    query = Catalogo.update().where(Catalogo.c.catalogo_id == catalogo_id).values(**catalogo.dict())
    await database.execute(query)
    return await database.fetch_one(Catalogo.select().where(Catalogo.c.catalogo_id == catalogo_id))

@router.delete("/catalogos/{catalogo_id}")
async def eliminar_catalogo(catalogo_id: int):
    query = Catalogo.select().where(Catalogo.c.catalogo_id == catalogo_id)
    db_catalogo = await database.fetch_one(query)
    if db_catalogo is None:
        raise HTTPException(status_code=404, detail="Catálogo no encontrado")
    await database.execute(Catalogo.delete().where(Catalogo.c.catalogo_id == catalogo_id))
    return {"detail": "Catálogo eliminado"}
