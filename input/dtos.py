from typing import List
from domain.models import Element, Subsystem, System
from calculations.reliability_structure import ReliabilityStructure


class ElementDTO:
    name: str
    damage_intensity: float
    repair_intensity: float

    def __init__(self, name, damage_intensity, repair_intensity):
        self.name = name
        self.damage_intensity = damage_intensity
        self.repair_intensity = repair_intensity

    def __repr__(self):
        return f"ElementDTO(name={self.name}, damage_intensity={self.damage_intensity}, " \
               f"repair_intensity={self.repair_intensity})"


class SubsystemDTO:
    name: str
    subsystem_type: ReliabilityStructure
    element_list: List[Element] = []

    def __init__(self, name, subsystem_type, elements):
        self.name = name
        self.subsystem_type = subsystem_type
        self.element_list = elements

    def __repr__(self):
        return f"SubsystemDTO(name={self.name}, subsystem_type={self.subsystem_type}, " \
               f"element_List={self.element_list})"


class SystemDTO:
    name: str
    system_type: ReliabilityStructure
    subsystem_list: List[Subsystem] = []

    def __init__(self, name, system_type, subsystems):
        self.name = name
        self.system_type = system_type
        self.subsystem_list = subsystems

    def __repr__(self):
        return f"SubsystemDTO(name={self.name}, system_type={self.system_type}, " \
               f"element_List={self.subsystem_list})"


class SimulationDTO:
    name: str
    system: System
    time_horizon: int
    time_change: int
    time_repair: int
    number_of_iterations: int

    def __init__(self, name, system, time_horizon, time_change, time_repair, number_of_iterations):
        self.name = name
        self.system = system
        self.time_horizon = time_horizon
        self.time_change = time_change
        self.time_repair = time_repair
        self.number_of_iterations = number_of_iterations

