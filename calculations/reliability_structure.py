from enum import Enum
from abc import ABC, abstractmethod
from typing import List


class ReliabilityStructure(Enum):
    """Enum contains basic reliability structures."""
    SERIAL_SUBSYSTEM = 'struktura szeregowa'
    PARALLEL_SUBSYSTEM = 'struktura równolegla'


class ReliabilityStructureStrategy(ABC):

    @abstractmethod
    def calculate_reliability_structure_state(self, list_of_states: List[bool]) -> bool:
        """Calculate structure state depending on reliability structure."""


class SerialReliabilityStructureStrategy(ReliabilityStructureStrategy):

    def calculate_reliability_structure_state(self, list_of_states: List[bool]) -> bool:
        return True if all(list_of_states) else False


class ParallelReliabilityStructureStrategy(ReliabilityStructureStrategy):

    def calculate_reliability_structure_state(self, list_of_states: List[bool]) -> bool:
        return True if any(list_of_states) else False

