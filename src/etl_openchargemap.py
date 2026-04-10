# Importar librerías
import pandas as pd

# Prueba simple: crear un DataFrame
data = {
    "Estacion": ["Carga 1", "Carga 2"],
    "Ciudad": ["Santiago", "Valparaíso"],
    "Potencia_kW": [50, 22]
}

df = pd.DataFrame(data)
print(df)

