from sqlalchemy import Table, Column, Integer, String, DateTime, ForeignKey, func, MetaData
from pydantic import BaseModel, Field
from typing import Optional

# Metadata compartida para todas las tablas
metadata = MetaData()

# Modelo SQLAlchemy: Tabla Album
Album = Table(
    "Album",
    metadata,
    Column("album_id", Integer, primary_key=True),
    Column("album_nombre", String(40), nullable=False),
    Column("artista_id", Integer, ForeignKey("Artista.artista_id"), nullable=True),
    Column("album_status", String(2), default='A'),  # 'A' (activo), 'I' (inactivo)
    Column("album_fecha_modificacion", DateTime, default=func.now(), onupdate=func.now())
)

# Esquema Pydantic: Base para Album
class AlbumBase(BaseModel):
    album_nombre: str = Field(..., max_length=40)
    artista_id: Optional[int] = None
    album_status: Optional[str] = "A"

# Esquema Pydantic: Crear Album
class AlbumCreate(AlbumBase):
    album_id:int

# Esquema Pydantic: Album en Base de Datos
class AlbumInDB(AlbumBase):
    album_id: int

    class Config:
        from_attributes = True
