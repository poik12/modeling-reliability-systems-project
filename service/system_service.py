from typing import List
from input.dtos import SystemDTO
from mapper.mappers import SystemMapper
from domain.models import System
from repository.system_repository import SystemRepository
from service.abstract_service import AbstractService


class SystemService(AbstractService):

    _system_repository = SystemRepository()
    _system_mapper = SystemMapper()

    def get_all_from_db(self) -> List[System]:
        system_entity_list = self._system_repository.find_all()
        system_object_list = []
        for system_entity in system_entity_list:
            system_object = self._system_mapper.map_from_entity_to_object(system_entity)
            system_object_list.append(system_object)
        return system_object_list

    def get_by_id_from_db(self, entity_id: int) -> System:
        system_from_db = self._system_repository.find_by_id(entity_id)
        return self._system_mapper.map_from_entity_to_object(system_from_db)

    def save_in_db(self, dto: SystemDTO) -> None:
        entity = self._system_mapper.map_from_dto_to_entity(dto)
        self._system_repository.save(entity)

    def update_by_id(self, dto: SystemDTO, entity_id: int) -> None:
        entity = self._system_mapper.map_from_dto_to_entity(dto)
        self._system_repository.update_by_id(entity, entity_id)

    def delete_by_id(self, entity_id: int) -> None:
        self._system_repository.delete_by_id(entity_id)


