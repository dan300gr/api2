from fastapi import FastAPI
from contextlib import asynccontextmanager
from db import database  # Asegúrate de que la importación esté correcta
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Configura los orígenes permitidos
origins = [
    "http://localhost:3000",  # Tu frontend local
    "https://musicstorefinal.onrender.com",  # Dominio de producción (si es necesario)
]

# Agrega el middleware de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Permite estos orígenes
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos HTTP
    allow_headers=["*"],  # Permite todas las cabeceras
)

# Lifespan para manejar el ciclo de vida de la app
@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    yield  # Permite continuar con la ejecución de la app
    await database.disconnect()

# Instancia de la app con lifespan
app = FastAPI(lifespan=lifespan)



# Incluye los routers
from routers.producto import router as producto_router
from routers.catalogo import router as catalogo_router
from routers.tipo_producto import router as tipo_producto_router
from routers.artista import router as artista_router
from routers.album import router as album_router
from routers.proveedor import router as proveedor_router
from routers.edificio import router as edificio_router
from routers.ubicacion import router as ubicacion_router
from routers.stock import router as stock_router
from routers.inventario import router as inventario_router

app.include_router(producto_router, prefix="/api", tags=["Productos"])
app.include_router(catalogo_router, prefix="/api", tags=["Catálogos"])
app.include_router(tipo_producto_router, prefix="/api", tags=["Tipos de Producto"])
app.include_router(artista_router, prefix="/api", tags=["Artistas"])
app.include_router(album_router, prefix="/api", tags=["Álbumes"])
app.include_router(proveedor_router, prefix="/api", tags=["Proveedores"])
app.include_router(edificio_router, prefix="/api", tags=["Edificios"])
app.include_router(ubicacion_router, prefix="/api", tags=["Ubicaciones"])
app.include_router(stock_router, prefix="/api", tags=["Stock"])
app.include_router(inventario_router, prefix="/api", tags=["Inventario"])

@app.get("/")
def root():
    return {"message": "Bienvenido a la API de Tienda de Música"}
