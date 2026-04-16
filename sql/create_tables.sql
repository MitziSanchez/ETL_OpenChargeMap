-- CREAR TABLAS

-- TABLA DE POIS - PUNTOS DE INTERES, ESTACIONES DE CARGA, LOCACIONES
CREATE TABLE pois(
	poi_id INT PRIMARY KEY,
 	name TEXT NOT NULL,
 	operator_id INT NOT NULL,
	country_id INT NOT NULL,
 	state_or_province TEXT, 
 	town TEXT,
 	address TEXT NOT NULL,
 	latitude DOUBLE PRECISION NOT NULL,
 	longitude DOUBLE PRECISION NOT NULL,
	status_type_id INT NOT NULL
)

-- TABLA PARA CONEXIONES. CONEXIONES QUE DISPONE CADA POI
CREATE TABLE connections(
	connection_id INT PRIMARY KEY,
	poi_id INT NOT NULL,
	status_type_id INT NOT NULL,
	connection_type_id INT NOT NULL,
	supply_type_id INT,
	amps DOUBLE PRECISION,
	voltage DOUBLE PRECISION,
	power_kw DOUBLE PRECISION,
	quantity INT
)

-- TABLA DE TIPOS DE CONEXIÓN
CREATE TABLE connection_types(
	connection_type_id INT PRIMARY KEY,
	name TEXT NOT NULL,
	is_obsolete BOOLEAN,
	is_discontinued BOOLEAN,
	formal_name TEXT
)

-- TABLA DE OPERADORES
CREATE TABLE operators(
	operator_id INT PRIMARY KEY,
	name TEXT NOT NULL,
	is_private_individual BOOLEAN,
	web_site_url TEXT
)

-- TABLA DE TIPOS DE ESTADO
CREATE TABLE status_types(
	status_type_id INT PRIMARY KEY,
	name TEXT NOT NULL	
)

-- TABLA DE TIPO DE SUMINISTRO
CREATE TABLE supply_types(
	supply_type_id INT PRIMARY KEY,
	name TEXT NOT NULL,
	description TEXT 
)

-- TABLA DE PAISES
CREATE TABLE countries(
	country_id INT PRIMARY KEY,
	name TEXT NOT NULL,
	continent_code CHAR(2) NOT NULL,
	iso_code CHAR(2) NOT NULL
)






