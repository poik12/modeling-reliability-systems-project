from typing import List

from input.dtos import SubsystemDTO
from mapper.mappers import SubsystemMapper
from domain.models import Subsystem
from repository.subsystem_repository import SubsystemRepository
from service.abstract_service import AbstractService


class SubsystemService(AbstractService):

    _subsystem_repository = SubsystemRepository()
    _subsystem_mapper = SubsystemMapper()

    def get_all_from_db(self) -> List[Subsystem]:
        subsystem_entity_list = self._subsystem_repository.find_all()
        subsystem_object_list = []
        for subsystem_entity in subsystem_entity_list:
            subsystem_object = self._subsystem_mapper.map_from_entity_to_object(subsystem_entity)
            subsystem_object_list.append(subsystem_object)
        return subsystem_object_list

    def get_by_id_from_db(self, entity_id: int) -> Subsystem:
        subsystem_from_db = self._subsystem_repository.find_by_id(entity_id)
        return self._subsystem_mapper.map_from_entity_to_object(subsystem_from_db)

    def save_in_db(self, dto: SubsystemDTO) -> None:
        entity = self._subsystem_mapper.map_from_dto_to_entity(dto)
        self._subsystem_repository.save(entity)

    def update_by_id(self, dto: SubsystemDTO, entity_id: int) -> None:
        entity = self._subsystem_mapper.map_from_dto_to_entity(dto)
        self._subsystem_repository.update_by_id(entity, entity_id)

    def delete_by_id(self, entity_id: int) -> None:
        self._subsystem_repository.delete_by_id(entity_id)



