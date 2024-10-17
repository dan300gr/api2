from fastapi import APIRouter, HTTPException
from db import database
from model.stock import Stock, StockCreate, StockInDB

router = APIRouter()

@router.post("/stocks/", response_model=StockInDB)
async def crear_stock(stock: StockCreate):
    query = Stock.insert().values(**stock.dict())
    try:
        last_record_id = await database.execute(query)
        return {**stock.dict(), "stock_id": last_record_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear el stock: {str(e)}")

@router.get("/stocks/{stock_id}", response_model=StockInDB)
async def leer_stock(stock_id: int):
    query = Stock.select().where(Stock.c.stock_id == stock_id)
    stock = await database.fetch_one(query)
    if stock is None:
        raise HTTPException(status_code=404, detail="Stock no encontrado")
    return stock

@router.get("/stocks/", response_model=list[StockInDB])
async def leer_stocks():
    query = Stock.select()
    stocks = await database.fetch_all(query)
    return stocks

@router.put("/stocks/{stock_id}", response_model=StockInDB)
async def actualizar_stock(stock_id: int, stock: StockCreate):
    query = Stock.update().where(Stock.c.stock_id == stock_id).values(**stock.dict())
    await database.execute(query)
    return await database.fetch_one(Stock.select().where(Stock.c.stock_id == stock_id))

@router.delete("/stocks/{stock_id}")
async def eliminar_stock(stock_id: int):
    query = Stock.select().where(Stock.c.stock_id == stock_id)
    db_stock = await database.fetch_one(query)
    if db_stock is None:
        raise HTTPException(status_code=404, detail="Stock no encontrado")
    await database.execute(Stock.delete().where(Stock.c.stock_id == stock_id))
    return {"detail": "Stock eliminado"}
