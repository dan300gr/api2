from sqlalchemy import Table, Column, Integer, String, DateTime, func, MetaData
from pydantic import BaseModel, Field
from typing import Optional

# Metadata para las tablas
metadata = MetaData()

# Modelo SQLAlchemy: Tabla Artista
Artista = Table(
    "Artista",
    metadata,
    Column("artista_id", Integer, primary_key=True),
    Column("artista_nombre", String(40), nullable=False),
    Column("artista_status", String(2), default='A'),  # 'A' (activo), 'I' (inactivo)
    Column("artista_fecha_modificacion", DateTime, default=func.now(), onupdate=func.now())
)

# Esquema Pydantic: Base para Artista
class ArtistaBase(BaseModel):
    artista_nombre: str = Field(..., max_length=40)
    artista_status: Optional[str] = "A"

# Esquema Pydantic: Crear Artista
class ArtistaCreate(ArtistaBase):
    artista_id: int

# Esquema Pydantic: Artista en Base de Datos
class ArtistaInDB(ArtistaBase):
    artista_id: int

    class Config:
        from_attributes = True
