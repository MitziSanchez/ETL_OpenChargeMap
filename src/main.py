# Importar loaders
from src.loaders.countries_loader import cargar_paises 
from src.loaders.supply_types_loader import cargar_tipos_suministro 
from src.loaders.operators_loader import cargar_operadores
from src.loaders.connection_types_loader import cargar_tipos_conexiones
from src.loaders.status_types_loader import cargar_tipos_estados
from src.loaders.pois_loader import cargar_pois

def etl_main():
    
    # Data referencial
    # cargar_paises()
    # cargar_tipos_suministro()
    # cargar_operadores()
    # cargar_tipos_conexiones()
    #cargar_tipos_estados()

    # Datos principales
    cargar_pois()

# Ejecutar 
if __name__ == "__main__":
    etl_main()    


