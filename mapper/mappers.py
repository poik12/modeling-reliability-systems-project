from datetime import datetime
from input.dtos import SubsystemDTO, ElementDTO, SimulationDTO, SystemDTO
from domain.models import Element, Subsystem, System, Simulation
from typing import Tuple
from abc import ABC, abstractmethod

from mapper.converters import ImageConversion
from output.graph_generator import GraphGeneration


class AbstractMapper(ABC):

    @abstractmethod
    def map_from_entity_to_object(self, entity: Tuple) -> object:
        """Map entity to model object."""

    @abstractmethod
    def map_from_dto_to_entity(self, dto: object) -> object:
        """Map dto to entity object in domain."""


class ElementMapper(AbstractMapper):

    def map_from_entity_to_object(self, entity: Tuple) -> Element:
        element_object = Element()
        element_object.id = entity[0]
        element_object.name = entity[1]
        element_object.damage_intensity = entity[2]
        element_object.repair_intensity = entity[3]
        element_object.created_on = entity[4]
        element_object.updated_on = entity[5]
        return element_object

    def map_from_dto_to_entity(self, dto: ElementDTO) -> Element:
        element_entity = Element()
        element_entity.name = dto.name
        element_entity.damage_intensity = dto.damage_intensity
        element_entity.repair_intensity = dto.repair_intensity
        element_entity.created_on = datetime.now()
        element_entity.updated_on = datetime.now()
        return element_entity


class SubsystemMapper(AbstractMapper):

    def map_from_entity_to_object(self, entity: Subsystem) -> Subsystem:
        subsystem_object = Subsystem()
        subsystem_object.id = entity.id
        subsystem_object.name = entity.name
        subsystem_object.created_on = entity.created_on
        subsystem_object.updated_on = entity.updated_on
        subsystem_object.reliability_structure = entity.reliability_structure
        subsystem_object.elements = entity.elements
        subsystem_object.element_list = entity.elements
        subsystem_object.number_of_elements = entity.number_of_elements
        subsystem_object.state = entity.state
        return subsystem_object

    def map_from_dto_to_entity(self, dto: SubsystemDTO) -> Subsystem:
        subsystem_entity = Subsystem()
        subsystem_entity.name = dto.name
        subsystem_entity.reliability_structure = dto.subsystem_type.value
        subsystem_entity.element_list = dto.element_list
        subsystem_entity.number_of_elements = len(dto.element_list)
        subsystem_entity.created_on = datetime.now()
        subsystem_entity.updated_on = datetime.now()
        return subsystem_entity


class SystemMapper(AbstractMapper):
    graph_generator = GraphGeneration()

    def map_from_entity_to_object(self, entity: System) -> System:
        system_object = System()
        system_object.id = entity.id
        system_object.name = entity.name
        system_object.reliability_structure = entity.reliability_structure
        system_object.subsystem_list = entity.subsystems
        system_object.subsystems = entity.subsystems
        system_object.number_of_subsystems = entity.number_of_subsystems
        system_object.created_on = entity.created_on
        system_object.updated_on = entity.updated_on
        ImageConversion.convert_binary_to_file(entity.system_graph, './controller/static/system_graph_from_db.png')
        return system_object

    def map_from_dto_to_entity(self, dto: SystemDTO) -> System:
        system_entity = System()
        system_entity.name = dto.name
        system_entity.reliability_structure = dto.system_type.value
        system_entity.subsystem_list = dto.subsystem_list
        system_entity.number_of_subsystems = len(dto.subsystem_list)
        system_entity.created_on = datetime.now()
        system_entity.updated_on = datetime.now()
        self.graph_generator.draw_graph(dto.subsystem_list, dto.system_type.value)
        system_entity.system_graph = ImageConversion.convert_file_to_binary('./output/graph_images/system_graph.png')
        return system_entity


class SimulationMapper(AbstractMapper):

    def map_from_entity_to_object(self, entity: Simulation) -> Simulation:
        system_object = Simulation()
        system_object.id = entity.id
        system_object.system_id = entity.system_id
        system_object.name = entity.name
        system_object.time_horizon = entity.time_horizon
        system_object.time_change = entity.time_change
        system_object.time_repair = entity.time_repair
        system_object.number_of_iterations = entity.number_of_iterations
        system_object.created_on = entity.created_on
        system_object.updated_on = entity.updated_on
        return system_object

    def map_from_dto_to_entity(self, dto: SimulationDTO) -> Simulation:
        simulation_entity = Simulation()
        simulation_entity.name = dto.name
        simulation_entity.system_id = dto.system.id
        simulation_entity.time_horizon = dto.time_horizon
        simulation_entity.time_change = dto.time_change
        simulation_entity.time_repair = dto.time_repair
        simulation_entity.number_of_iterations = dto.number_of_iterations
        simulation_entity.created_on = datetime.now()
        simulation_entity.updated_on = datetime.now()
        return simulation_entity
