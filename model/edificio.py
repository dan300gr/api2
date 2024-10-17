from sqlalchemy import Table, Column, Integer, String, DateTime, func, MetaData
from pydantic import BaseModel, Field
from typing import Optional

# Metadata para las tablas
metadata = MetaData()

# Modelo SQLAlchemy: Tabla Edificio
Edificio = Table(
    "Edificio",
    metadata,
    Column("edificio_id", Integer, primary_key=True),
    Column("edificio_nombre", String(40), nullable=False),
    Column("edificio_direccion", String(40), nullable=True),
    Column("edificio_status", String(2), default='A'),  # 'A' (activo), 'I' (inactivo)
    Column("edificio_fecha_modificacion", DateTime, default=func.now(), onupdate=func.now())
)

# Esquema Pydantic: Base para Edificio
class EdificioBase(BaseModel):
    edificio_nombre: str = Field(..., max_length=40)
    edificio_direccion: Optional[str] = None
    edificio_status: Optional[str] = "A"

# Esquema Pydantic: Crear Edificio
class EdificioCreate(EdificioBase):
    edificio_id:int

# Esquema Pydantic: Edificio en Base de Datos
class EdificioInDB(EdificioBase):
    edificio_id: int

    class Config:
        from_attributes = True
