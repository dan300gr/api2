from sqlalchemy import Table, Column, Integer, String, DateTime, func, MetaData
from pydantic import BaseModel, Field, EmailStr
from typing import Optional

# Metadata para las tablas
metadata = MetaData()

# Modelo SQLAlchemy: Tabla Proveedor
Proveedor = Table(
    "Proveedor",
    metadata,
    Column("proveedor_id", Integer, primary_key=True),
    Column("proveedor_nombre", String(40), nullable=False),
    Column("proveedor_direccion", String(40), nullable=True),
    Column("proveedor_telefono", String(20), nullable=True),
    Column("proveedor_correo", String(40), nullable=True),
    Column("proveedor_status", String(2), default='A'),  # 'A' (activo), 'I' (inactivo)
    Column("proveedor_fecha_modificacion", DateTime, default=func.now(), onupdate=func.now())
)

# Esquema Pydantic: Base para Proveedor
class ProveedorBase(BaseModel):
    proveedor_nombre: str = Field(..., max_length=40)
    proveedor_direccion: Optional[str] = None
    proveedor_telefono: Optional[str] = Field(None, max_length=20)
    proveedor_correo: Optional[EmailStr] = None
    proveedor_status: Optional[str] = "A"

# Esquema Pydantic: Crear Proveedor
class ProveedorCreate(ProveedorBase):
    proveedor_id:int
# Esquema Pydantic: Proveedor en Base de Datos
class ProveedorInDB(ProveedorBase):
    proveedor_id: int

    class Config:
        from_attributes = True
