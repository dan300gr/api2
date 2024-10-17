from sqlalchemy import Table, Column, Integer, ForeignKey, String, DateTime, func, MetaData
from pydantic import BaseModel, Field
from typing import Optional

metadata = MetaData()

# Modelo SQLAlchemy: Tabla Inventario
Inventario = Table(
    "Inventario",
    metadata,
    Column("inventario_id", Integer, primary_key=True),  # Este es el ID de inventario
    Column("ubicacion_id", Integer, ForeignKey("Ubicacion.ubicacion_id"), nullable=False),
    Column("producto_id", Integer, ForeignKey("Producto.producto_id"), nullable=False),
    Column("stock_id", Integer, ForeignKey("Stock.stock_id"), nullable=False),  # Referencia a Stock
    Column("inventario_cantidad", Integer, nullable=False, default=0),
    Column("inventario_status", String(2), default='A'),
    Column("inventario_fecha_modificacion", DateTime, default=func.now(), onupdate=func.now())
)

# Esquema Pydantic: Base para Inventario
class InventarioBase(BaseModel):
    ubicacion_id: int
    producto_id: int
    stock_id: int
    inventario_cantidad: int = Field(..., ge=0)  # Asegura que la cantidad no sea negativa
    inventario_status: Optional[str] = "A"

# Esquema Pydantic: Crear Inventario
class InventarioCreate(InventarioBase):
    inventario_id:int

# Esquema Pydantic: Inventario en Base de Datos
class InventarioInDB(InventarioBase):
    inventario_id: int

    class Config:
        from_attributes = True
