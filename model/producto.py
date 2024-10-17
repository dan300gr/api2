from sqlalchemy import Table, Column, Integer, String, DateTime, DECIMAL, ForeignKey, func, MetaData
from pydantic import BaseModel, Field
from typing import Optional

# Metadata para las tablas
metadata = MetaData()

# Modelo SQLAlchemy: Tabla Producto
Producto = Table(
    "Producto",
    metadata,
    Column("producto_id", Integer, primary_key=True),
    Column("producto_nombre", String(40), nullable=False),
    Column("producto_precio", DECIMAL(18, 2), nullable=False),
    Column("tipo_id", Integer, ForeignKey("TipoProducto.tipo_id"), nullable=False),
    Column("catalogo_id", Integer, ForeignKey("Catalogo.catalogo_id"), nullable=False),
    Column("album_id", Integer, ForeignKey("Album.album_id"), nullable=False),
    Column("producto_status", String(2), default='A'),  # 'A' (activo), 'I' (inactivo)
    Column("producto_fecha_modificacion", DateTime, default=func.now(), onupdate=func.now())
)

# Esquema Pydantic: Base para Producto
class ProductoBase(BaseModel):
    producto_nombre: str = Field(..., max_length=40)
    producto_precio: float
    tipo_id: int
    catalogo_id: int
    album_id: int
    producto_status: Optional[str] = "A"

# Esquema Pydantic: Crear Producto
class ProductoCreate(ProductoBase):
    producto_id: int  # Incluir producto_id aquí

# Esquema Pydantic: Producto en Base de Datos
class ProductoInDB(ProductoBase):
    producto_id: int

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True  # Permitir tipos arbitrarios
