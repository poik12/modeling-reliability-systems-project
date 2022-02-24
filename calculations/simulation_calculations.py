from typing import List
import numpy as np
from calculations.system_calculations import SystemCalc
from domain.models import Simulation, Subsystem
from output.chart_generator import ChartGeneration
from service.simulation_service import SimulationService
from service.subsystem_service import SubsystemService


class SimulationCalc:
    simulation_id: int
    _simulation: Simulation
    _simulation_service = SimulationService()
    _subsystem_service = SubsystemService()
    _system_calc: SystemCalc
    _chart_generator: ChartGeneration
    subsystem_list: List[Subsystem]

    def __init__(self, simulation_id):
        self._simulation = self._simulation_service.get_by_id_from_db(simulation_id)
        self._system_calc = SystemCalc(self._simulation.system_id)
        self._chart_generator = ChartGeneration(
            self._simulation.id,
            self._time_horizon_vector(),
            self._time_repair_vector()
        )
        self.subsystem_list = self._get_subsystem_list()

    def calculate_simulation(self):
        self._failure_and_repair_probability_density()
        self._calculate_system_state()

    def _time_horizon_vector(self):
        return np.linspace(0, self._simulation.time_horizon, self._simulation.time_horizon)

    def _time_repair_vector(self):
        return np.linspace(0, self._simulation.time_repair, self._simulation.time_horizon)

    def _failure_and_repair_probability_density(self):
        failure_probability_density_dict = self._system_calc.failure_probability_density_for_each_element(
            self._time_horizon_vector()
        )
        repair_probability_density_dict = self._system_calc.repair_probability_density_for_each_element(
            self._time_repair_vector()
        )

        self._chart_generator.draw_density_charts(failure_probability_density_dict, repair_probability_density_dict)

    def _get_subsystem_list(self):
        subsystem_list = []
        for subsystem in self._simulation.system.subsystems:
            subsystem = self._subsystem_service.get_by_id_from_db(subsystem.id)
            subsystem_list.append(subsystem)
        return subsystem_list

    def _calculate_system_state(self):
        system_state_list = np.zeros(self._simulation.number_of_iterations, dtype=bool)
        num_of_successful_iter_list = np.zeros(self._simulation.number_of_iterations)
        relative_time = int(self._simulation.time_horizon / self._simulation.time_change)

        num_of_successful_iter_in_time_list = []
        [num_of_successful_iter_in_time_list.append(np.append(0, i)) for i in range(relative_time)]
        num_of_successful_iter_in_time_list = np.asarray(num_of_successful_iter_in_time_list)

        for iter_number in range(self._simulation.number_of_iterations - 1):
            num_of_successful_iter = 0

            subsystem_list = self.subsystem_list
            current_system_state = True
            self._system_calc.set_state_of_elements_to_true(subsystem_list)

            for time in range(relative_time):

                current_system_state, current_subsystem_list = self._system_calc.calculate_current_system_state(
                    subsystem_list,
                    time
                )

                subsystem_list = current_subsystem_list

                if not current_system_state:
                    break

                num_of_successful_iter += 1
                num_of_successful_iter_in_time_list[time][0] += 1

            system_state_list = np.append(system_state_list, current_system_state)
            num_of_successful_iter_list = np.append(num_of_successful_iter_list, num_of_successful_iter)

        # Draw histogram
        self._chart_generator.draw_histogram_chart(num_of_successful_iter_list, self._simulation.time_horizon / 5)

        # Calculate empirical functions
        empirical_reliability_function_values = self._system_calc.calculate_empirical_reliability_function(
            num_of_successful_iter_in_time_list,
            self._simulation.number_of_iterations
        )
        empirical_failure_function_values = self._system_calc.calculate_empirical_failure_function(
            empirical_reliability_function_values
        )

        # Draw empiric function charts
        self._chart_generator.draw_empirical_charts(
            empirical_failure_function_values,
            empirical_reliability_function_values,
            self._time_horizon_vector()
        )



