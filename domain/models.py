from datetime import datetime
from typing import List

from sqlalchemy import Table, Column, String, DateTime, Integer, Float, ForeignKey, BLOB
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from domain.database_connection import DatabaseConnection

# Connect to Database
database_connector = DatabaseConnection()
database_connector.get_connection_to_database()

# Create Database
Base = declarative_base()

# Many to many relationship
subsystems_elements = Table('subsystems_elements', Base.metadata,
                            Column('subsystem_id', ForeignKey('subsystems.id'), primary_key=False),
                            Column('element_id', ForeignKey('elements.id'), primary_key=False))

systems_subsystems = Table('systems_subsystems', Base.metadata,
                           Column('system_id', ForeignKey('systems.id'), primary_key=False),
                           Column('subsystem_id', ForeignKey('subsystems.id'), primary_key=False))


# Model Classes
class Element(Base):
    __tablename__ = 'elements'

    id = Column('id', Integer(), primary_key=True)
    name = Column('name', String(100), nullable=False)
    damage_intensity = Column('damage_intensity', Float(), nullable=False)
    repair_intensity = Column('repair_intensity', Float(), nullable=False)
    created_on = Column('created_on', DateTime(), default=datetime.now())
    updated_on = Column('updated_on', DateTime(), default=datetime.now(), onupdate=datetime.now())
    state: bool = True

    def __repr__(self):
        return f'Element(id={self.id}, name={self.name}, damage_intensity={self.damage_intensity}, ' \
               f'repair_intensity={self.repair_intensity}, state={self.state}, ' \
               f'created_on={self.created_on}, updated_on={self.updated_on})'

    def __eq__(self, other):
        return self.id == other.id


class Subsystem(Base):
    __tablename__ = 'subsystems'

    id = Column('id', Integer(), primary_key=True)
    name = Column('name', String(100), nullable=False)
    reliability_structure = Column('reliability_structure', String(100), nullable=False)
    number_of_elements = Column('number_of_elements', Integer())
    created_on = Column('created_on', DateTime(), default=datetime.now())
    updated_on = Column('updated_on', DateTime(), default=datetime.now(), onupdate=datetime.now())
    elements = relationship("Element", secondary=subsystems_elements)
    element_list: List[Element] = list()
    state: bool = True

    def __repr__(self):
        return f'Subsystem(id={self.id}, name={self.name}, reliability_structure={self.reliability_structure},' \
               f' state={self.state}, created_on={self.created_on}, updated_on={self.updated_on}, ' \
               f' number_of_elements={self.number_of_elements}, element_list={self.element_list})'

    def __eq__(self, other):
        return self.id == other.id


class System(Base):
    __tablename__ = 'systems'

    id = Column('id', Integer(), primary_key=True)
    name = Column('name', String(100), nullable=False)
    reliability_structure = Column('reliability_structure', String(100), nullable=False)
    number_of_subsystems = Column('number_of_subsystems', Integer())
    created_on = Column('created_on', DateTime(), default=datetime.now())
    updated_on = Column('updated_on', DateTime(), default=datetime.now(), onupdate=datetime.now())
    subsystems = relationship("Subsystem", secondary=systems_subsystems)
    system_graph = Column('system_graph', BLOB())
    subsystem_list: List[Subsystem] = list()
    state: bool = True

    def __repr__(self):
        return f'System(id={self.id}, name={self.name}, reliability_structure={self.reliability_structure},' \
               f' state={self.state}, created_on={self.created_on}, updated_on={self.updated_on}, ' \
               f' number_of_subsystems={self.number_of_subsystems}, subsystem_list={self.subsystem_list})'


class Simulation(Base):
    __tablename__ = 'simulations'

    id = Column('id', Integer(), primary_key=True)
    name = Column('name', String(100), nullable=False)
    system_id = Column(Integer(), ForeignKey('systems.id'))
    time_horizon = Column('time_horizon', Integer(), nullable=False)
    time_change = Column('time_change', Integer(), nullable=False)
    time_repair = Column('time_repair', Integer(), nullable=False)
    number_of_iterations = Column('number_of_iterations', Integer(), nullable=False)
    created_on = Column('created_on', DateTime(), default=datetime.now())
    updated_on = Column('updated_on', DateTime(), default=datetime.now(), onupdate=datetime.now())
    system: System

    def __repr__(self):
        return f'Simulation(id={self.id}, name={self.name}, system_id={self.system_id}, system={self.system}' \
               f' created_on={self.created_on}, updated_on={self.updated_on}, ' \
               f' time_horizon={self.time_horizon}, time_change={self.time_change},' \
               f' time_repair={self.time_repair}, number_of_iterations={self.number_of_iterations})'


# Add / update entities in database
database_engine = database_connector.get_engine()
Base.metadata.create_all(database_engine)
