-- CLAVES FORANEAS, RELACIONES

-- CONNECTIONS -> POIS
ALTER TABLE connections
ADD CONSTRAINT fk_connections_pois
FOREIGN KEY (poi_id) REFERENCES pois(poi_id)

-- CONNECTIONS -> STATUS TYPE
ALTER TABLE connections
ADD CONSTRAINT fk_connections_status_types
FOREIGN KEY (status_type_id) REFERENCES status_types(status_type_id)

-- CONNECTIONS -> CONNECTION TYPE
ALTER TABLE connections
ADD CONSTRAINT fk_connections_connection_types
FOREIGN KEY (connection_type_id) REFERENCES connection_types(connection_type_id)

-- CONNECTIONS -> SUPPLY TYPE
ALTER TABLE connections
ADD CONSTRAINT fk_connections_supply_types
FOREIGN KEY (supply_type_id) REFERENCES supply_types(supply_type_id)

-- POIS -> OPERADORES 
ALTER TABLE pois
ADD CONSTRAINT fk_pois_operators
FOREIGN KEY (operator_id) REFERENCES operators(operator_id)

-- POIS -> COUNTRIES
ALTER TABLE pois
ADD CONSTRAINT fk_pois_countries
FOREIGN KEY (country_id) REFERENCES countries(country_id)
