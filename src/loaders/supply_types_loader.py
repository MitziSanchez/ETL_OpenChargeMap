# =======================================================
# Obtener tipos de suministro de la data referencial
# =======================================================

import requests
import json
from src.config import API_URL_REF, API_KEY, get_Connection
import pandas as pd

def cargar_tipos_suministro():
        
    print("\nOBTENER DATOS DE TIPOS DE SUMINISTRO DESDE API---------------") 

    # Obtener datos de la API
    url_ref = API_URL_REF
    params_ref = {
        "output": "json",          
        "key": API_KEY          
    }

    response_ref = requests.get(url_ref, params = params_ref)
    data_ref = response_ref.json()
    t_sum = data_ref["CurrentTypes"]

    #print("\nt_sum[0]:")
    #print(json.dumps(t_sum[0], indent=4)) 
    print(f"> Registros de suministro obtenidos: {len(t_sum)}")

    if len(t_sum) == 0:
        print("> No se han insertado datos")

    else:

        # Convertir en dataframe (Obtener todas las columnas)
        df_t_sum = pd.json_normalize(t_sum)
                
        # Revisar duplicados (ID)
        filas_duplicadas = df_t_sum.duplicated(subset=["ID"]).sum()
        print(f"> Filas duplicadas (ID): {filas_duplicadas}")

        # Eliminar duplicados
        if filas_duplicadas > 0:               
            df_t_sum = df_t_sum.drop_duplicates(subset=["ID"])
                
        print(f"> Registros de suministro totales: {len(df_t_sum)}")  

        # Revisar valores nulos
        col_obligatorias = ["ID","Title"]

        filas_nulos_ob = df_t_sum[col_obligatorias].isnull().any(axis=1).sum()
        print(f"> Valores nulos en columnas obligatorias: {filas_nulos_ob}")

        # Si existen filas con nulos, transforma
        if filas_nulos_ob > 0:

            # Eliminar filas con id nulo
            df_t_sum = df_t_sum.dropna(subset=["ID"])

            # Reemplazar filas con title nulo
            df_t_sum["Title"] = df_t_sum["Title"].fillna("No informado") 

        print(f"> Total de registros limpios: {len(df_t_sum)}")
        # print(df_t_sum.head())

        # Carga de datos a PostgreSQL
        cargar_bd(df_t_sum)
              

      
def cargar_bd(df_t_sum):

    conn = None
    cursor = None

    try:

        print("> Inicia proceso insercion a base de datos")
        # Obtener conexion
        conn = get_Connection()
        cursor = conn.cursor()

        # Insertar registros
        for _, row in df_t_sum.iterrows():
            cursor.execute(
                """
                INSERT INTO supply_types(supply_type_id, name, description)
                VALUES(%s, %s, %s)
                ON CONFLICT(supply_type_id) DO NOTHING;
                """,
                (row["ID"], row["Title"], row.get("Description"))
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
        

    


    
    
    