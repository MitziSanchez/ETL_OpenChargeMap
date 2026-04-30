# =======================================================
# Obtener conexiones
# =======================================================

import requests
import json
from src.config import API_KEY, API_URL_POI, get_session
import pandas as pd 
from src.models import Connection

def cargar_conexiones():

    print("\nOBTENER CONEXIONES DESDE API---------------") 

    # Obtener datos de la API - POIS EN CHILE, PAIS ID 49
    url_poi = API_URL_POI
    params_poi = {
        "output": "json",      
        "countryid" : [49],
        "maxresults": 500,         
        "key": API_KEY           
    }

    response_poi = requests.get(url_poi, params = params_poi)
    data_pois = response_poi.json()

    # print("\npois[0]:")
    # print(json.dumps(data_pois[0], indent=4))

    # print("\npois[0].Connections[0]:")
    # print(json.dumps(data_pois[0]["Connections"][0], indent=4))

    print(f"> Registros de pois obtenidos: {len(data_pois)}")     
    conexiones_len = sum(len(poi["Connections"]) for poi in data_pois)
    print(f"> Registros de conexiones obtenidos: {conexiones_len}")
        
    if conexiones_len == 0:
        print("> No se han insertado datos")
    else:

        # Convertir en dataframe. Seleccionar solo los datos necesarios
        df_conexiones = pd.json_normalize(
            data_pois,
            record_path = "Connections",
            meta = ["ID"],
            meta_prefix = "Poi_"
        )
        
        df_conexiones = df_conexiones[["ID","Poi_ID","StatusTypeID","ConnectionTypeID","CurrentTypeID","Amps","Voltage","PowerKW","Quantity"]]
        # print(df_conexiones.head())

        # Revisar IDs duplicados
        filas_duplicadas = df_conexiones.duplicated(subset=["ID"]).sum()
        print(f"> Filas duplicadas (ID): {filas_duplicadas}")

        # Eliminar filas duplicadas
        if filas_duplicadas > 0:
            df_conexiones = df_conexiones.drop_duplicates(subset=["ID"])
            
        print(f"> Registros de conexiones totales: {len(df_conexiones)}")  

        # Revisar nulos 
        col_criticas = [
            "ID", 
            "Poi_ID", 
            "StatusTypeID",
            "ConnectionTypeID"  
        ]
        filas_nulos = df_conexiones[col_criticas].isnull().any(axis=1).sum()
        print(f"> Valores nulos en columnas críticas: {filas_nulos}")

        # Si existen filas con valores nulos
        if filas_nulos > 0:

            # Eliminar filas con ID nulo
            df_conexiones = df_conexiones.dropna(subset=["ID"])

            # Eliminar filas con Poi_ID nulo
            df_conexiones = df_conexiones.dropna(subset=["Poi_ID"])

            # Reemplazar valores nulos en status type id - 0 corresponde Unknown
            df_conexiones["StatusTypeID"] = df_conexiones["StatusTypeID"].fillna(0)

            # Reemplazar valores nulos en connection type id - 0 corresponde Unknown
            df_conexiones["ConnectionTypeID"] = df_conexiones["ConnectionTypeID"].fillna(0)       


        # Convertir current type id a entero permitiendo nulos
        df_conexiones["CurrentTypeID"] = df_conexiones["CurrentTypeID"].astype("Int64")

        # Convertir quantity a entero perimitiendo nulos
        df_conexiones["Quantity"] = df_conexiones["Quantity"].astype("Int64")
        # df_conexiones["Quantity"] = df_conexiones["Quantity"].apply(lambda x: int(x) if pd.notnull(x) else None)

        # Reemplazar valores nan por none en todo el dataframe. Para el resto de columnas pueden ser nulas        
        df_conexiones = df_conexiones.astype(object).where(pd.notnull(df_conexiones), None)        

        # print(df_conexiones.dtypes)
        # print(df_conexiones.head())
        print(f"> Total de registros limpios: {len(df_conexiones)}")

        cargar_bd(df_conexiones)


def cargar_bd(df_conexiones):

    # Cargar a bd utilizando libreria SQLAlchemy

    try:
        print("> Inicia proceso inserción a base de datos")
         
        session = get_session()

        # Insertar dataframe en la tabla conexiones, se usara inserción fila a fila, ya que se controlara reemplazos de filas existentes
        for _, row in df_conexiones.iterrows():
            conexion = Connection(
                connection_id = row["ID"],
                poi_id = row["Poi_ID"],
                status_type_id = row["StatusTypeID"],
                connection_type_id = row["ConnectionTypeID"],
                supply_type_id = row["CurrentTypeID"],
                amps = row["Amps"],
                voltage = row["Voltage"],
                power_kw = row["PowerKW"],
                quantity = row["Quantity"]
            )

            # Inserta o actualiza si el registro ya existe
            session.merge(conexion)
        
        session.commit()
        print("> Inserción de datos a PostgreSQL realizada")

    except Exception as e:
        session.rollback()
        print(f"X Ha ocurrido un error: {e}")

    finally:
        #Cerrar conexion
        if session:
            session.close()

        print("> Conexión cerrada")
