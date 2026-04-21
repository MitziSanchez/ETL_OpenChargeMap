# Importar loaders
from src.loaders.countries_loader import cargar_paises 
from src.loaders.supply_types_loader import cargar_tipos_suministro 

def etl_main():
    
    cargar_paises()
    cargar_tipos_suministro()
    

# Ejecutar 
if __name__ == "__main__":
    etl_main()    


