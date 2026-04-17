-- Database: open_charge_map

-- DROP DATABASE IF EXISTS open_charge_map;

CREATE DATABASE open_charge_map
    WITH
    OWNER = your_db_owner
    ENCODING = 'UTF8'
    LC_COLLATE = 'Spanish_Spain.1252'
    LC_CTYPE = 'Spanish_Spain.1252'
    LOCALE_PROVIDER = 'libc'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1
    IS_TEMPLATE = False;

COMMENT ON DATABASE open_charge_map
    IS 'Base de datos destinada a almacenar los datos extraídos desde API OpenChargeMap por ETL_OpenChargeMap. Contiene datos de estaciones de carga para vehículos eléctricos en Chile.';