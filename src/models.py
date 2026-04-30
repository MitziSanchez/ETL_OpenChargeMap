# =======================================================
# Modelos para tablas de bd para SQLAlchemy
# =======================================================

from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Poi(Base):
    __tablename__ = 'pois'

    poi_id = Column(Integer, primary_key=True)
    name = Column(String)
    operator_id = Column(Integer)
    country_id = Column(Integer)
    state_or_province = Column(String, nullable=True)
    town = Column(String, nullable=True)
    address = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    status_type_id = Column(Integer)

    # Relación con conexiones
    connections = relationship("Connection", back_populates="poi")

class Connection(Base):
    __tablename__ = 'connections'

    connection_id = Column(Integer, primary_key=True)
    poi_id = Column(Integer, ForeignKey('pois.poi_id'))
    status_type_id = Column(Integer)
    connection_type_id = Column(Integer)
    supply_type_id = Column(Integer, nullable=True)
    amps = Column(Float, nullable=True)
    voltage = Column(Float, nullable=True)
    power_kw = Column(Float, nullable=True)
    quantity = Column(Integer, nullable=True)

    # Relación con pois
    poi = relationship("Poi", back_populates="connections")