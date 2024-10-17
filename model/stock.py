from sqlalchemy import Table, Column, Integer, ForeignKey, String, DateTime, func, MetaData
from pydantic import BaseModel, Field
from typing import Optional

# Metadata para las tablas
metadata = MetaData()

# Modelo SQLAlchemy: Tabla Stock
Stock = Table(
    "Stock",
    metadata,
    Column("stock_id", Integer, primary_key=True),
    Column("producto_id", Integer, ForeignKey("Producto.producto_id"), nullable=False),
    Column("stock_cantidad", Integer, nullable=False, default=0),  # Cantidad total en stock
    Column("stock_status", String(2), default='A'),  # 'A' (activo), 'I' (inactivo)
    Column("stock_fecha_modificacion", DateTime, default=func.now(), onupdate=func.now())
)

# Esquema Pydantic: Base para Stock
class StockBase(BaseModel):
    producto_id: int
    stock_cantidad: int = Field(..., gt=0)  # Debe ser mayor que 0
    stock_status: Optional[str] = "A"

# Esquema Pydantic: Crear Stock
class StockCreate(StockBase):
    stock_id:int

# Esquema Pydantic: Stock en Base de Datos
class StockInDB(StockBase):
    stock_id: int

    class Config:
        from_attributes = True
