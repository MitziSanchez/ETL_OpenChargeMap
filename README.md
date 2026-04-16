# ETL_OpenChargeMap

## Descripción del proyecto
Desarrollo de ETL para extracción de datos desde API Open Charge Map (Puntos de carga para vehículos eléctricos) y carga de datos en base de datos de PostgreSQL.


## Objetivos del proyecto
- Obtener datos de los puntos de carga para vehículos electricos de Chile. 
- Visualizar las concentraciones de estos puntos para determinar las zonas con mayor disponibilidad de estaciones de carga electrica.

## Stack tecnológico
- API Open Charge Map (https://openchargemap.org)
- Anaconda
- Python 
- Jupyter Notebooks
- PostgreSQL
- GitHub

## Conceptos importantes
- **EVSE:** 
- **POI:** Point of interest, punto de interés. Lugar geografico con estaciones EVSE.

## Desarollo

### Creación de entorno 
Crear el entorno con anaconda:
``` bash
conda create -n etl_openchargemap python=3.11
conda activate openchargemap
```

Considerar el archivo **archivo** para la carga de librerias.

### Conexión y exploración de datos de API Open Charge Map
Generación de notebook con Jupyter, archivo **api_exploracion.ipynb**.
Se exploran los datos entregados por la api. Considera la revisión de la estructura, la limpieza y transformación de acuerdo a lo necesario.
- Considera la extracción de los puntos de carga disponibles en Chile.
- Se extraen los campos necesarios referente a lo siguiente:
    - Estaciones de carga y puntos de conexion.
    - Operadores que manejan dichas estaciones.
    - Tipos de connexiones, suministro y estados.

### Modelo de datos es PostgreSQL
Una vez explorados los datos y determinado el set necesario para el análisis. Se define el modelo de datos:

### Carga de datos a Base de datos 




