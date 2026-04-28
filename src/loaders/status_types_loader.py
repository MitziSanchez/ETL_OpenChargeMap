# =======================================================
# Obtener tipos de estados de la data referencial
# =======================================================

import requests
import json
from src.config import API_KEY, API_URL_REF, get_Connection
import pandas as pd 

def cargar_tipos_estados():

    print("\nOBTENER DATOS DE TIPOS DE ESTADOS DESDE API---------------") 

    # Obtener datos de la API
    url_ref = API_URL_REF
    params_ref = {
        "output": "json",          
        "key": API_KEY          
    }

    response_ref = requests.get(url_ref, params = params_ref)
    data_ref = response_ref.json()
    tipos_estados = data_ref["StatusTypes"]

    # print("\ntipos_estados[0]:")
    # print(json.dumps(tipos_estados[0], indent=4)) 
    print(f"> Registros de tipos de estados obtenidos: {len(tipos_estados)}")
    
    if len(tipos_estados) == 0:
        print("> No se han insertado datos")
    else:

        # Convertir en dataframe
        df_tipos_estados = pd.json_normalize(tipos_estados)
        df_tipos_estados = df_tipos_estados[["ID","Title"]]
        # print(df_tipos_estados.head())

        # Revisar IDs duplicados
        filas_duplicadas = df_tipos_estados.duplicated(subset=["ID"]).sum()
        print(f"> Filas duplicadas (ID): {filas_duplicadas}")

        # Eliminar filas duplicadas
        if filas_duplicadas > 0:
            df_tipos_estados = df_tipos_estados.drop_duplicates(subset=["ID"])
            
        print(f"> Registros de tipos de estados totales: {len(df_tipos_estados)}")  

        # Revisar nulos 
        col_criticas = ["ID","Title"]
        filas_nulos = df_tipos_estados[col_criticas].isnull().any(axis=1).sum()
        print(f"> Valores nulos en columnas criticas: {filas_nulos}")

        # Si existen filas con valores nulos
        if filas_nulos > 0:

            # Eliminar filas con ID nulo
            df_tipos_estados = df_tipos_estados.dropna(subset=["ID"])

            # Reemplazar valores nulos en title
            df_tipos_estados["Title"] = df_tipos_estados["Title"].fillna("No informado")                                   
        
        print(f"> Total de registros limpios: {len(df_tipos_estados)}")
        # print(df_tipos_estados.head())

        # Carga de datos en postgre
        cargar_bd(df_tipos_estados)

    
def cargar_bd(df_tipos_estados):

    conn = None
    cursor = None

    try:
        print("> Inicia proceso insercion a base de datos")

        # Obtener conexion 
        conn = get_Connection()
        cursor = conn.cursor()

        # Insertar registros, si el registro existe, lo actualiza
        for _, row in df_tipos_estados.iterrows():
            cursor.execute(
                """
                INSERT INTO status_types (status_type_id, name)
                VALUES (%s, %s)
                ON CONFLICT(status_type_id) DO UPDATE SET 
                    name = EXCLUDED.name;
                """,
                (row["ID"], row["Title"])
            )
   
        # Confirmar cambios
        conn.commit()
        print("> Insercion de datos a PostgreSQL realizada")

    except Exception as e:
        print(f"X Ha ocurrido un error: {e}")

        # Si esta la conexion, aplica rollback
        if conn:
            conn.rollback()

    finally:
        #Cerrar conexion
        if cursor:
            cursor.close()

        if conn:
            conn.close()

        print("> Conexion cerrada")