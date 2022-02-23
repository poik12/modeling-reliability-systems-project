from typing import List

from input.dtos import SimulationDTO
from mapper.mappers import SimulationMapper
from domain.models import Simulation
from repository.simulation_repository import SimulationRepository
from service.abstract_service import AbstractService
from service.system_service import SystemService


class SimulationService(AbstractService):

    _system_service = SystemService()
    _simulation_repository = SimulationRepository()
    _simulation_mapper = SimulationMapper()

    def get_all_from_db(self) -> List[Simulation]:
        simulation_entity_list = self._simulation_repository.find_all()
        simulation_object_list = []
        for simulation_entity in simulation_entity_list:
            system_object = self._simulation_mapper.map_from_entity_to_object(simulation_entity)
            system_object.system = self._system_service.get_by_id_from_db(system_object.system_id)
            simulation_object_list.append(system_object)
        return simulation_object_list

    def get_by_id_from_db(self, entity_id: int) -> Simulation:
        simulation_from_db = self._simulation_repository.find_by_id(entity_id)
        simulation_object = self._simulation_mapper.map_from_entity_to_object(simulation_from_db)
        simulation_object.system = self._system_service.get_by_id_from_db(simulation_object.system_id)
        return simulation_object

    def save_in_db(self, dto: SimulationDTO) -> None:
        entity = self._simulation_mapper.map_from_dto_to_entity(dto)
        self._simulation_repository.save(entity)

    def update_by_id(self, dto: SimulationDTO, entity_id: int) -> None:
        entity = self._simulation_mapper.map_from_dto_to_entity(dto)
        self._simulation_repository.update_by_id(entity, entity_id)

    def delete_by_id(self, entity_id: int) -> None:
        self._simulation_repository.delete_by_id(entity_id)

