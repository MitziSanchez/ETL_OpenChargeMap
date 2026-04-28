# =======================================================
# Obtener operadores de la data referencial
# =======================================================

import requests
import json
from src.config import API_KEY, API_URL_REF, get_Connection
import pandas as pd 

def cargar_operadores():

    print("\nOBTENER DATOS DE OPERADORES DESDE API---------------") 

    # Obtener datos de la API
    url_ref = API_URL_REF
    params_ref = {
        "output": "json",          
        "key": API_KEY          
    }

    response_ref = requests.get(url_ref, params = params_ref)
    data_ref = response_ref.json()
    operadores = data_ref["Operators"]

    # print("\nOperadores[0]:")
    # print(json.dumps(operadores[0], indent=4)) 
    print(f"> Registros de operadores obtenidos: {len(operadores)}")
    
    if len(operadores) == 0:
        print("> No se han insertado datos")
    else:

        # Convertir en dataframe. Solo columnas necesarias 
        df_operadores = pd.json_normalize(operadores)
        df_operadores = df_operadores[["ID", "Title", "IsPrivateIndividual", "WebsiteURL"]]
        # print(df_operadores.head())

        # Revisar IDs duplicados
        filas_duplicadas = df_operadores.duplicated(subset=["ID"]).sum()
        print(f"> Filas duplicadas (ID): {filas_duplicadas}")

        # Eliminar filas duplicadas
        if filas_duplicadas > 0:
            df_operadores = df_operadores.drop_duplicates(subset=["ID"])
            
        print(f"> Registros de operadores totales: {len(df_operadores)}")  

        # Revisar nulos 
        col_criticas = ["ID","Title"]
        filas_nulos = df_operadores[col_criticas].isnull().any(axis=1).sum()
        print(f"> Valores nulos en columnas criticas: {filas_nulos}")

        # Si existen filas con valores nulos
        if filas_nulos > 0:

            # Eliminar filas con ID nulo
            df_operadores = df_operadores.dropna(subset=["ID"])

            # Reemplazar valores nulos en title
            df_operadores["Title"] = df_operadores["Title"].fillna("No informado")    

        # Reemplazar valores nulos en websiteURL por valores vacios
        df_operadores["WebsiteURL"] = df_operadores["WebsiteURL"].fillna("")                           
        
        print(f"> Total de registros limpios: {len(df_operadores)}")
        # print(df_operadores.head())

        # Carga de datos en postgre
        cargar_bd(df_operadores)

    
def cargar_bd(df_operadores):

    conn = None
    cursor = None

    try:
        print("> Inicia proceso insercion a base de datos")

        # Obtener conexion 
        conn = get_Connection()
        cursor = conn.cursor()

        # Insertar registros, si el registro existe, lo actualiza
        for _, row in df_operadores.iterrows():
            cursor.execute(
                """
                INSERT INTO operators (operator_id, name, is_private_individual, web_site_url)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT(operator_id) DO UPDATE SET 
                    name = EXCLUDED.name, 
                    is_private_individual = EXCLUDED.is_private_individual, 
                    web_site_url = EXCLUDED.web_site_url;
                """,
                (row["ID"], row["Title"], row.get("isPrivateIndividual"), row["WebsiteURL"])
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