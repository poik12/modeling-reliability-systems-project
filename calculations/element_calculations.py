from typing import List
from domain.models import Element, Subsystem
import numpy as np


class ElementCalc:

    @staticmethod
    def failure_probability_density(element: Element, time):
        return element.damage_intensity * np.exp(-element.damage_intensity * time)

    @staticmethod
    def repair_probability_density(element: Element, time):
        return element.repair_intensity * np.exp(-element.repair_intensity * time)

    @staticmethod
    def calculate_subsystem_state(subsystem: Subsystem, time: float) -> List[bool]:

        element_state_list = []
        for element in subsystem.elements:
            rnd_spoilage = 10 * (- 1 / element.damage_intensity) * np.log(1 - np.random.uniform(0, 1))
            rnd_repair = 10 * (- 1 / element.repair_intensity) * np.log(1 - np.random.uniform(0, 1))

            probability_of_spoilage = 1 - np.exp(-element.damage_intensity * time)
            probability_of_repair = 1 - np.exp(-element.repair_intensity * time)

            if element.state:
                if probability_of_spoilage > rnd_spoilage:
                    element.state = False
            else:
                if probability_of_repair > rnd_repair:
                    element.state = True
            element_state_list.append(element.state)

        return element_state_list

