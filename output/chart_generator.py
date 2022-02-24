import matplotlib.pyplot as plt
import matplotlib
import numpy as np
from service.simulation_service import SimulationService
from domain.models import Simulation


class ChartGeneration:
    # Font parameters
    font = {'family': 'DeJaVu Sans',
            'weight': 'bold',
            'size': 16}
    matplotlib.rc('font', **font)

    simulation_service = SimulationService()
    simulation: Simulation
    simulation_id: int
    time_horizon_vector: np.ndarray
    repair_horizon_vector: np.ndarray

    def __init__(self, simulation_id, time_horizon_vector, time_repair_vector):
        self.simulation = self.simulation_service.get_by_id_from_db(simulation_id)
        self.time_horizon_vector = time_horizon_vector
        self.time_repair_vector = time_repair_vector

    def draw_density_charts(self, failure_probability_density_dict, repair_probability_density_dict):
        self._draw_failure_probability_density(failure_probability_density_dict)
        self._draw_repair_probability_density(repair_probability_density_dict)

    def draw_empirical_charts(self, empirical_failure_values , empirical_reliability_values, time_horizon):
        self._draw_empirical_failure_function(empirical_failure_values, time_horizon)
        self._draw_empirical_reliability_function(empirical_reliability_values, time_horizon)

    def draw_histogram_chart(self, num_of_successful_iter, time_horizon):
        self._draw_histogram(num_of_successful_iter, time_horizon)

    def _draw_failure_probability_density(self, failure_probability_density_dict: dict):
        plt.figure(1, figsize=(14, 7))
        for element_id_key, failure_probability_density_value in failure_probability_density_dict.items():
            plt.plot(self.time_horizon_vector, failure_probability_density_value,
                     label='%s' % element_id_key)
        plt.legend()
        plt.xlabel('Czas [dzień]')
        plt.ylabel('Gęstość prawdopodobieństwa [-]')
        plt.title('Gęstość prawdopodobieństwa uszkodzenia', )
        plt.grid(True)
        plt.savefig('output/chart_images/failure_probability_density_chart.png')
        plt.savefig('./controller/static/failure_probability_density_chart.png')
        plt.close()

    def _draw_repair_probability_density(self, repair_probability_density_dict: dict):
        plt.figure(2, figsize=(14, 7))
        for element_id_key, repair_probability_density_value in repair_probability_density_dict.items():
            plt.plot(self.time_repair_vector, repair_probability_density_value,
                     label='%s' % element_id_key)
        plt.legend()
        plt.xlabel('Czas [dzień]')
        plt.ylabel('Gęstość prawdopodobieństwa [-]')
        plt.title('Gęstość prawdopodobieństwa odnowy')
        plt.grid(True)
        plt.savefig('output/chart_images/repair_probability_density_chart.png')
        plt.savefig('./controller/static/repair_probability_density_chart.png')
        plt.close()

    def _draw_empirical_reliability_function(self, empirical_reliability_values: np.ndarray, time_horizon: np.ndarray):
        plt.figure(3, figsize=(14, 7))
        plt.plot(time_horizon, empirical_reliability_values)
        plt.xlabel('Czas [dzień]')
        plt.ylabel('Niezawodność [-]')
        plt.title('Empiryczna funkcja niezawodności')
        plt.grid(True)
        plt.savefig('output/chart_images/empirical_reliability_function_chart.png')
        plt.savefig('./controller/static/empirical_reliability_function_chart.png')
        plt.close()

    def _draw_empirical_failure_function(self, empirical_failure_values: np.ndarray, time_horizon: np.ndarray):
        plt.figure(4, figsize=(14, 7))
        plt.plot(time_horizon, empirical_failure_values)
        plt.xlabel('Czas [dzień]')
        plt.ylabel('Zawodność [-]')
        plt.title('Dystrybuanta')
        plt.grid(True)
        plt.savefig('output/chart_images/empirical_failure_function_chart.png')
        plt.savefig('./controller/static/empirical_failure_function_chart.png')
        plt.close()

    def _draw_histogram(self, num_of_successful_iter: np.ndarray, time_horizon: int):
        plt.figure(5, figsize=(14, 7))
        plt.hist(num_of_successful_iter, bins=int(time_horizon))
        plt.xlabel('Czas do uszkodzenia systemu [dzień]')
        plt.ylabel('Liczebność przedziału [-]')
        plt.title('Histogram')
        plt.grid(True)
        plt.savefig('output/chart_images/histogram.png')
        plt.savefig('./controller/static/histogram.png')
        plt.close()
