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

    # Convertir en dataframe
    df_paises = pd.json_normalize(paises)

    # Renombrar columnas 
    
    
    
