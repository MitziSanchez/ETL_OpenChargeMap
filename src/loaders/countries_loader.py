# Obtener paises de la data referencial

import requests
import json
from src.config import API_URL_REF, API_KEY, get_Connection
import pandas as pd

def cargar_paises():
        
    print("\nOBTENER DATOS DE PAISES DESDE API---------------") 

    # Obtener datos de la API
    url_ref = API_URL_REF
    params_ref = {
        "output": "json",          
        "key": API_KEY          
    }

    response_ref = requests.get(url_ref, params = params_ref)
    data_ref = response_ref.json()
    paises = data_ref["Countries"]

    #print("\nPaises[0]:")
    #print(json.dumps(paises[0], indent=4)) 
    print(f"> Registros de paises obtenidos: {len(paises)}")

    if len(paises) == 0:
        print("> No se han insertado datos")
    else:

        # Convertir en dataframe (Obtener todas las columnas)
        df_paises = pd.json_normalize(paises)

        # Revisar IDs duplicados
        filas_duplicadas = df_paises.duplicated(subset=["ID"]).sum()
        print(f"> Filas duplicadas (ID): {filas_duplicadas}")

        # Eliminar filas duplicadas
        if filas_duplicadas > 0:
            df_paises = df_paises.drop_duplicates(subset=["ID"])
            
        print(f"> Registros de paises totales: {len(df_paises)}")  

        # Revisar nulos 
        col_obligatorias = ["ID","Title","ISOCode"]
        filas_nulos_ob = df_paises[col_obligatorias].isnull().any(axis=1).sum()
        print(f"> Valores nulos en columnas obligatorias: {filas_nulos_ob}")

        # Si existen filas con valores nulos
        if filas_nulos_ob > 0:

            # Eliminar filas con ID nulo
            df_paises = df_paises.dropna(subset=["ID"])

            # Reemplazar valores nulos en title
            df_paises["Title"] = df_paises["Title"].fillna("No informado")

            # Reemplazar valores nulos en Iso Code, valor en blanco
            df_paises["ISOCode"] = df_paises["ISOCode"].fillna("") 

        # Reemplazar valores nulos en continentCode, valor en blanco. BD permite nulos, pero se optara por reemplazar valores
        df_paises["ContinentCode"] = df_paises["ContinentCode"].fillna("")               
        
        print(f"> Total de registros limpios: {len(df_paises)}")
        # print(df_paises.head())

        # Carga de datos en postgre
        cargar_bd(df_paises)

    
def cargar_bd(df_paises):

    conn = None
    cursor = None

    try:
        print("> Inicia proceso insercion a base de datos")

        # Obtener conexion 
        conn = get_Connection()
        cursor = conn.cursor()

        # Insertar registros, actualiza los existentes
        for _, row in df_paises.iterrows():
            cursor.execute(
                """
                INSERT INTO countries (country_id, name, continent_code, iso_code)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT(country_id) DO UPDATE SET 
                    name = EXCLUDED.name,
                    continent_code = EXCLUDED.continent_code,
                    iso_code = EXCLUDED.iso_code;
                """,
                (row["ID"], row["Title"], row.get("ContinentCode"), row["ISOCode"])
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
        
    
    
    
