from sqlalchemy import create_engine, MetaData
from databases import Database

# Configura la URL de tu base de datos
DATABASE_URL = "mysql+pymysql://uvp:Duxg1_400@34.95.154.41:3306/MusicStore"

# Instancia de la base de datos para usar con async/await
database = Database(DATABASE_URL)

# Metadata para manejar las tablas
metadata = MetaData()

# Motor de SQLAlchemy para ejecutar acciones sobre la base de datos
engine = create_engine(DATABASE_URL)

# Crear todas las tablas definidas en los modelos si no existen
metadata.create_all(engine)
