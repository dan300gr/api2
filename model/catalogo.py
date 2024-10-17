from sqlalchemy import Table, Column, Integer, String, DateTime, func, MetaData
from pydantic import BaseModel, Field
from typing import Optional

# Metadata compartida para todas las tablas
metadata = MetaData()

# Modelo SQLAlchemy: Tabla Catalogo
Catalogo = Table(
    "Catalogo",
    metadata,
    Column("catalogo_id", Integer, primary_key=True),
    Column("catalogo_nombre", String(40), nullable=False),
    Column("catalogo_status", String(2), default='A'),  # 'A' (activo), 'I' (inactivo)
    Column("catalogo_fecha_modificacion", DateTime, default=func.now(), onupdate=func.now())
)

# Esquema Pydantic: Base para Catalogo
class CatalogoBase(BaseModel):
    catalogo_nombre: str = Field(..., max_length=40)
    catalogo_status: Optional[str] = "A"

# Esquema Pydantic: Crear Catalogo
class CatalogoCreate(CatalogoBase):
    catalogo_id: int  # Asegúrate de incluir el catalogo_id aquí

# Esquema Pydantic: Catalogo en Base de Datos
class CatalogoInDB(CatalogoBase):
    catalogo_id: int

    class Config:
        from_attributes = True
