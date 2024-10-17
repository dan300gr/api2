from sqlalchemy import Table, Column, Integer, String, DateTime, ForeignKey, func, MetaData
from pydantic import BaseModel, Field
from typing import Optional

# Metadata para las tablas
metadata = MetaData()

# Modelo SQLAlchemy: Tabla Ubicacion
Ubicacion = Table(
    "Ubicacion",
    metadata,
    Column("ubicacion_id", Integer, primary_key=True),
    Column("ubicacion_nombre", String(40), nullable=False),
    Column("edificio_id", Integer, ForeignKey("Edificio.edificio_id"), nullable=True),
    Column("ubicacion_status", String(2), default='A'),  # 'A' (activo), 'I' (inactivo)
    Column("ubicacion_fecha_modificacion", DateTime, default=func.now(), onupdate=func.now())
)

# Esquema Pydantic: Base para Ubicacion
class UbicacionBase(BaseModel):
    ubicacion_nombre: str = Field(..., max_length=40)
    edificio_id: Optional[int] = None
    ubicacion_status: Optional[str] = "A"

# Esquema Pydantic: Crear Ubicacion
class UbicacionCreate(UbicacionBase):
    ubicacion_id:int

# Esquema Pydantic: Ubicacion en Base de Datos
class UbicacionInDB(UbicacionBase):
    ubicacion_id: int

    class Config:
        from_attributes = True
