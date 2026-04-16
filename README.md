# ETL_OpenChargeMap

## Descripción del proyecto
Desarrollo de ETL para extracción de datos desde API Open Charge Map (Puntos de carga para vehículos eléctricos) y carga de datos en base de datos de PostgreSQL.


## Objetivos del proyecto
- Construir un ETL básico que permita extraer datos desde la API Open Charge Map, transformarlos y almacenarlos en PostgreSQL, generando una base estructurada que permita futuros análisis sobre infraestructura de electromovilidad en Chile. 


## Stack tecnológico
- API Open Charge Map (https://openchargemap.org)
- Anaconda
- Python 
- Jupyter Notebooks
- PostgreSQL
- GitHub

## Conceptos importantes
- **EVSE:** (Electric Vehicle Supply Equipment), Conjunto de hardware y software que transfiere energía de forma segura desde la red eléctrica a la batería de un vehículo eléctrico o híbrido enchufable. Se les conoce por diversos nombres, tales como: cargadores, estaciones de carga o puntos de carga.
- **POI:** (Point of interest), punto de interés. Estaciones de servicio de carga EVSE.

## Desarollo

### Creación de entorno 
Crear el entorno con anaconda:
``` bash
conda create -n etl_openchargemap python=3.11
conda activate openchargemap
```

### Conexión y exploración de datos de API Open Charge Map
Generación de notebook con Jupyter, archivo **api_exploracion.ipynb**.
Se exploran los datos entregados por la api. Considera la revisión de la estructura, la limpieza y transformación de acuerdo a lo necesario.
- Extracción de los puntos de carga disponibles en Chile.
- Extracción de datos de referencia:
    - Estaciones de carga y puntos de conexion.
    - Operadores.
    - Tipos de conexiones, suministro y estados.
    - Paises.

### Modelo de datos es PostgreSQL
Una vez explorados los datos y determinado el set necesario para el análisis, se define y construye el modelo de datos: 

![MOodeloBD](sql/Diagrama_BD_OpenChargeMap.jpg)

Se debe tener en consideración la siguiente equivalendia de datos de la API con el modelo:

> **Tipos de conecciones** <br>
> Tipo de conexión para usuario final con soporte EVSE. Hace referencia al tipo de enchufe.<br>
> API: ConnectionTypes <br>
> BD: connection_types <br>

> **Operadores** <br>
> Empresa u organización que controla la red de puntos de carga. <br>
> API: Operators <br>
> BD: operators <br>

> **Tipos de estados** <br>
> Estado de una locación o tipo de equipamiento que indica si esta actualmente operativa. <br>
> API: StatusTypes <br>
> BD: status_types <br>

> **Tipos de suministro** <br>
> Correspode al tipo de suministro de corriente eléctrica. <br>
> API: CurrentTypes <br>
> BD: supply_types <br>

> **Pois** <br>
> Puntos de interes. Estaciones de servicio con puntos de carga EVSE. <br>
> API: poi <br>
> BD: pois <br>

> **Conexiones** <br>
> Cargadores disponibles en las estaciones de servicio (Pois). <br>
> API: Connections <br>
> BD: connections <br>




