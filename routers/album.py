from fastapi import APIRouter, HTTPException
from db import database
from model.album import Album, AlbumCreate, AlbumInDB

router = APIRouter()

@router.post("/albumes/", response_model=AlbumInDB)
async def crear_album(album: AlbumCreate):
    # Verificar si el album_id ya existe
    query = Album.select().where(Album.c.album_id == album.album_id)
    existing_album = await database.fetch_one(query)

    if existing_album:
        raise HTTPException(status_code=400, detail="El ID del álbum ya existe")

    # Insertar el nuevo álbum
    query = Album.insert().values(
        album_id=album.album_id,  # Usar el ID proporcionado
        album_nombre=album.album_nombre,
        artista_id=album.artista_id,  # Usar el ID del artista proporcionado
        album_status=album.album_status
    )

    try:
        await database.execute(query)
        return {**album.dict()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear el álbum: {str(e)}")

@router.get("/albumes/{album_id}", response_model=AlbumInDB)
async def leer_album(album_id: int):
    query = Album.select().where(Album.c.album_id == album_id)
    album = await database.fetch_one(query)
    if album is None:
        raise HTTPException(status_code=404, detail="Álbum no encontrado")
    return album

@router.get("/albumes/", response_model=list[AlbumInDB])
async def leer_albumes():
    query = Album.select()
    albumes = await database.fetch_all(query)
    return albumes

@router.put("/albumes/{album_id}", response_model=AlbumInDB)
async def actualizar_album(album_id: int, album: AlbumCreate):
    query = Album.update().where(Album.c.album_id == album_id).values(**album.dict())
    await database.execute(query)
    return await database.fetch_one(Album.select().where(Album.c.album_id == album_id))

@router.delete("/albumes/{album_id}")
async def eliminar_album(album_id: int):
    query = Album.select().where(Album.c.album_id == album_id)
    db_album = await database.fetch_one(query)
    if db_album is None:
        raise HTTPException(status_code=404, detail="Álbum no encontrado")
    await database.execute(Album.delete().where(Album.c.album_id == album_id))
    return {"detail": "Álbum eliminado"}
