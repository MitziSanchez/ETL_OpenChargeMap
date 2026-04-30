# =======================================================
# Obtener tipos de conexiones de la data referencial
# =======================================================

import requests
import json
from src.config import API_KEY, API_URL_REF, get_Connection
import pandas as pd 

def cargar_tipos_conexiones():

    print("\nOBTENER TIPOS DE CONEXIONES DESDE API---------------") 

    # Obtener datos de la API
    url_ref = API_URL_REF
    params_ref = {
        "output": "json",          
        "key": API_KEY          
    }

    response_ref = requests.get(url_ref, params = params_ref)
    data_ref = response_ref.json()
    tipos_conexiones = data_ref["ConnectionTypes"]

    # print("\ntipos_conexiones[0]:")
    # print(json.dumps(tipos_conexiones[0], indent=4)) 
    print(f"> Registros de tipos de conexiones obtenidos: {len(tipos_conexiones)}")
    
    if len(tipos_conexiones) == 0:
        print("> No se han insertado datos")
    else:

        # Convertir en dataframe
        df_tipos_conexiones = pd.json_normalize(tipos_conexiones)
        # print(df_tipos_conexiones.head())

        # Revisar IDs duplicados
        filas_duplicadas = df_tipos_conexiones.duplicated(subset=["ID"]).sum()
        print(f"> Filas duplicadas (ID): {filas_duplicadas}")

        # Eliminar filas duplicadas
        if filas_duplicadas > 0:
            df_tipos_conexiones = df_tipos_conexiones.drop_duplicates(subset=["ID"])
            
        print(f"> Registros de tipos de conexiones totales: {len(df_tipos_conexiones)}")  

        # Revisar nulos 
        col_criticas = ["ID","Title"]
        filas_nulos = df_tipos_conexiones[col_criticas].isnull().any(axis=1).sum()
        print(f"> Valores nulos en columnas críticas: {filas_nulos}")

        # Si existen filas con valores nulos
        if filas_nulos > 0:

            # Eliminar filas con ID nulo
            df_tipos_conexiones = df_tipos_conexiones.dropna(subset=["ID"])

            # Reemplazar valores nulos en title
            df_tipos_conexiones["Title"] = df_tipos_conexiones["Title"].fillna("No informado")    

        # Definir nulos reconocibles para formalName
        df_tipos_conexiones["FormalName"] = df_tipos_conexiones["FormalName"].astype(object).where(
            pd.notnull(df_tipos_conexiones["FormalName"]), None
        )

        print(f"> Total de registros limpios: {len(df_tipos_conexiones)}")
        # print(df_tipos_conexiones.head())

        # Carga de datos en postgre
        cargar_bd(df_tipos_conexiones)

    
def cargar_bd(df_tipos_conexiones):

    conn = None
    cursor = None

    try:
        print("> Inicia proceso inserción a base de datos")

        # Obtener conexion 
        conn = get_Connection()
        cursor = conn.cursor()

        # Insertar registros, si el registro existe, lo actualiza
        for _, row in df_tipos_conexiones.iterrows():
            cursor.execute(
                """
                INSERT INTO connection_types (connection_type_id, name, is_obsolete, is_discontinued, formal_name)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT(connection_type_id) DO UPDATE SET 
                    name = EXCLUDED.name, 
                    is_obsolete = EXCLUDED.is_obsolete, 
                    is_discontinued = EXCLUDED.is_discontinued, 
                    formal_name = EXCLUDED.formal_name;
                """,
                (row["ID"], row["Title"], row.get("IsObsolete"), row.get("IsDiscontinued"), row["FormalName"])
            )
   
        # Confirmar cambios
        conn.commit()
        print("> Inserción de datos a PostgreSQL realizada")

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

        print("> Conexión cerrada")