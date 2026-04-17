# Configuración del proyecto

# Librerias
from dotenv import load_dotenv
import os

# libreria ostgre
import psycopg2

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

# Connección bd
def get_Connection():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )