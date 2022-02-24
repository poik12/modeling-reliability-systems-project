from typing import List
import numpy as np
from calculations.element_calculations import ElementCalc
from calculations.reliability_structure import ReliabilityStructureStrategy, SerialReliabilityStructureStrategy, \
    ParallelReliabilityStructureStrategy, ReliabilityStructure
from domain.models import System, Subsystem
from service.subsystem_service import SubsystemService
from service.system_service import SystemService


class SystemCalc:
    system_id: int
    system: System
    system_service = SystemService()
    subsystem_service = SubsystemService()
    element_calc = ElementCalc()
    reliability_structure_strategy: ReliabilityStructureStrategy

    def __init__(self, system_id):
        self.system = self.system_service.get_by_id_from_db(system_id)

    def failure_probability_density_for_each_element(self, time_horizon_vector: np.ndarray) -> dict:
        failure_probability_density_dict = {}
        for subsystem in self.system.subsystem_list:
            subsystem_from_db = self.subsystem_service.get_by_id_from_db(subsystem.id)
            for element in subsystem_from_db.element_list:
                failure_probability_density_vector = ElementCalc.failure_probability_density(
                    element, time_horizon_vector
                )
                failure_probability_density_dict[element.name] = failure_probability_density_vector
        return failure_probability_density_dict

    def repair_probability_density_for_each_element(self, time_repair_vector: np.ndarray) -> dict:
        repair_probability_density_dict = {}
        for subsystem in self.system.subsystem_list:
            subsystem_from_db = self.subsystem_service.get_by_id_from_db(subsystem.id)
            for element in subsystem_from_db.element_list:
                repair_probability_density_vector = ElementCalc.repair_probability_density(
                    element, time_repair_vector
                )
                repair_probability_density_dict[element.name] = repair_probability_density_vector
        return repair_probability_density_dict

    def set_state_of_elements_to_true(self, subsystem_list: List[Subsystem]) -> None:
        for subsystem in subsystem_list:
            for element in subsystem.element_list:
                element.state = True

    def calculate_current_system_state(self, subsystem_list: List[Subsystem], time: float) -> tuple[bool, list[Subsystem]]:
        subsystem_state_list = []
        current_subsystem_list = self._calculate_current_subsystem_state(subsystem_list,  time)
        for subsystem in current_subsystem_list:
            subsystem_state_list.append(subsystem.state)

        if self.system.reliability_structure == ReliabilityStructure.SERIAL_SUBSYSTEM.value:
            self.reliability_structure_strategy = SerialReliabilityStructureStrategy()
        else:
            self.reliability_structure_strategy = ParallelReliabilityStructureStrategy()
        current_system_state = self.reliability_structure_strategy.calculate_reliability_structure_state(subsystem_state_list)
        return current_system_state, current_subsystem_list

    def _calculate_current_subsystem_state(self, subsystem_list: List[Subsystem],  time: float) -> List[Subsystem]:
        # subsystem_states_list = []
        current_subsystem_list = []
        for subsystem in subsystem_list:
            element_states_list = self.element_calc.calculate_subsystem_state(subsystem, time)

            if subsystem.reliability_structure == ReliabilityStructure.SERIAL_SUBSYSTEM.value:
                self.reliability_structure_strategy = SerialReliabilityStructureStrategy()
            else:
                self.reliability_structure_strategy = ParallelReliabilityStructureStrategy()
            current_subsystem_state = self.reliability_structure_strategy.calculate_reliability_structure_state(element_states_list)
            subsystem.state = current_subsystem_state
            current_subsystem_list.append(subsystem)
            # subsystem_states_list.append(current_subsystem_state)
        return current_subsystem_list

    def calculate_empirical_reliability_function(self, successful_iter: np.ndarray, number_of_iter: int) -> List[float]:
        empirical_reliability_value_list = []
        length = len(successful_iter)
        [empirical_reliability_value_list.append(successful_iter[i][0] / number_of_iter) for i in range(length)]
        return empirical_reliability_value_list

    def calculate_empirical_failure_function(self, empirical_reliability_value_list: list[float]) -> List[float]:
        empirical_failure_value_list = []
        [empirical_failure_value_list.append(1 - value) for value in empirical_reliability_value_list]
        return empirical_failure_value_list

