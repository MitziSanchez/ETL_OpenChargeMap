# =======================================================
# Configuraciones del proyecto
# =======================================================

# Para trabajar con variables de entorno
from dotenv import load_dotenv
import os

# Para trabajar con postgre
import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

#Obtener variables de entorno
load_dotenv()

# API
API_URL_POI = "https://api.openchargemap.io/v3/poi"
API_URL_REF = "https://api.openchargemap.io/v3/referencedata"
API_KEY = os.getenv("API_KEY")

# BD 
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# Conexion bd, psycopg2 para datos referenciales
def get_Connection():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

# Conexion bd, SQLAlchemy para datos principales
def get_engine():   
    DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
    return create_engine(DATABASE_URL)

def get_session():
    engine = get_engine()
    SessionLocal = sessionmaker(bind=engine)
    return SessionLocal()