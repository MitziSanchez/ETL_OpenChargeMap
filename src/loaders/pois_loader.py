# =======================================================
# Obtener POIs 
# =======================================================

import requests
import json
from src.config import API_KEY, API_URL_POI, get_session
import pandas as pd 
from src.models import Poi

def cargar_pois():

    print("\nOBTENER POIS DESDE API---------------") 

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
    print(f"> Registros de pois obtenidos: {len(data_pois)}")
    
    if len(data_pois) == 0:
        print("> No se han insertado datos")
    else:

        # Convertir en dataframe. Seleccionar solo los datos necesarios
        df_pois = pd.json_normalize(data_pois)
        df_pois = df_pois[[
            "ID", 
            "AddressInfo.Title", 
            "OperatorID",
            "AddressInfo.CountryID",
            "AddressInfo.StateOrProvince",
            "AddressInfo.Town", 
            "AddressInfo.AddressLine1",
            "AddressInfo.AddressLine2",
            "AddressInfo.Latitude",
            "AddressInfo.Longitude",
            "StatusTypeID"                
        ]]
        
        # print(df_pois.head())

        # Revisar IDs duplicados
        filas_duplicadas = df_pois.duplicated(subset=["ID"]).sum()
        print(f"> Filas duplicadas (ID): {filas_duplicadas}")

        # Eliminar filas duplicadas
        if filas_duplicadas > 0:
            df_pois = df_pois.drop_duplicates(subset=["ID"])
            
        print(f"> Registros de pois totales: {len(df_pois)}")  

        # Revisar nulos 
        col_criticas = [
            "ID", 
            "AddressInfo.Title", 
            "OperatorID",
            "AddressInfo.CountryID",
            "AddressInfo.Latitude",
            "AddressInfo.Longitude",
            "StatusTypeID"     
        ]
        filas_nulos = df_pois[col_criticas].isnull().any(axis=1).sum()
        print(f"> Valores nulos en columnas críticas: {filas_nulos}")

        # Si existen filas con valores nulos
        if filas_nulos > 0:

            # Eliminar filas con ID nulo
            df_pois = df_pois.dropna(subset=["ID"])

            # Reemplazar valores nulos en title
            df_pois["AddressInfo.Title"] = df_pois["AddressInfo.Title"].fillna("No informado") 

            # Reemplazar valores nulos en OperatorID - 1 corresponde Unknown Operator
            df_pois["OperatorID"] = df_pois["OperatorID"].fillna(1)

            # Eliminar filas con CountryID nulo
            df_pois = df_pois.dropna(subset=["AddressInfo.CountryID"])  

            # Eliminar filas con Latitude o Longitude nulo) 
            df_pois = df_pois.dropna(subset=["AddressInfo.Latitude"])
            df_pois = df_pois.dropna(subset=["AddressInfo.Longitude"])

            # Reemplazar valores nulos en StatusTypeID - 0 corresponde Unknown
            df_pois["StatusTypeID"] = df_pois["StatusTypeID"].fillna(0)


        # Unir address line 1 y 2 en una sola columna
        df_pois["Address"] = (df_pois["AddressInfo.AddressLine1"].fillna("") + " " + df_pois["AddressInfo.AddressLine2"].fillna("")).str.strip()
        # print(df_pois[["AddressInfo.AddressLine1", "AddressInfo.AddressLine2", "Address"]].head())

        # Eliminar las columnas concatenadas
        df_pois = df_pois.drop(columns = ["AddressInfo.AddressLine1","AddressInfo.AddressLine2"])  

        # Reemplazar valores nan por none en todo el dataframe. Para el resto de columnas pueden ser nulas        
        df_pois = df_pois.astype(object).where(pd.notnull(df_pois), None)   

        print(f"> Total de registros limpios: {len(df_pois)}")
        # print(df_pois.head())       

        cargar_bd(df_pois)


def cargar_bd(df_pois):

    # Cargar a bd utilizando libreria SQLAlchemy

    try:
        print("> Inicia proceso inserción a base de datos")
         
        session = get_session()

        # Insertar dataframe en la tabla pois, se usara insercion fila a fila, ya que se controlara reemplazos de filas existentes
        for _, row in df_pois.iterrows():
            poi = Poi(
                poi_id = row["ID"],
                name = row["AddressInfo.Title"],
                operator_id = row["OperatorID"],
                country_id = row["AddressInfo.CountryID"],
                state_or_province = row["AddressInfo.StateOrProvince"],
                town = row["AddressInfo.Town"],
                address = row["Address"],
                latitude = row["AddressInfo.Latitude"],
                longitude = row["AddressInfo.Longitude"],
                status_type_id = row["StatusTypeID"]
            )

            # Inserta o actualiza si el registro ya existe
            session.merge(poi)
        
        session.commit()
        print("> Inserción de datos a PostgreSQL realizada")

    except Exception as e:
        session.rollback()
        print(f"X Ha ocurrido un error: {e}")

    finally:
        #Cerrar conexión
        if session:
            session.close()

        print("> Conexión cerrada")
