from sqlalchemy import Table, Column, Integer, String, DateTime, func, MetaData
from pydantic import BaseModel, Field
from typing import Optional

# Metadata para las tablas
metadata = MetaData()

# Modelo SQLAlchemy: Tabla TipoProducto
TipoProducto = Table(
    "TipoProducto",
    metadata,
    Column("tipo_id", Integer, primary_key=True),
    Column("tipo_nombre", String(40), nullable=False, unique=True),
    Column("tipo_status", String(2), default='A'),  # 'A' (activo), 'I' (inactivo)
    Column("tipo_fecha_modificacion", DateTime, default=func.now(), onupdate=func.now())
)

# Esquema Pydantic: Base para TipoProducto
class TipoProductoBase(BaseModel):
    tipo_nombre: str = Field(..., max_length=40)
    tipo_status: Optional[str] = "A"

# Esquema Pydantic: Crear TipoProducto
class TipoProductoCreate(TipoProductoBase):
    tipo_id: int  # Asegúrate de incluir el tipo_id aquí

# Esquema Pydantic: TipoProducto en Base de Datos
class TipoProductoInDB(TipoProductoBase):
    tipo_id: int

    class Config:
        from_attributes = True

