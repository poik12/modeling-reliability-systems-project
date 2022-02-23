from typing import List
from mapper.mappers import ElementMapper
from domain.models import Element
from repository.element_repository import ElementRepository
from service.abstract_service import AbstractService
from input.dtos import ElementDTO


class ElementService(AbstractService):
    _element_repository = ElementRepository()
    _element_mapper = ElementMapper()

    def get_all_from_db(self) -> List[Element]:
        element_entity_list = self._element_repository.find_all()
        element_object_list = []
        for element_entity in element_entity_list:
            element_object = self._element_mapper.map_from_entity_to_object(element_entity)
            element_object_list.append(element_object)
        return element_object_list

    def get_by_id_from_db(self, entity_id: int) -> Element:
        element_entity = self._element_repository.find_by_id(entity_id)
        return self._element_mapper.map_from_entity_to_object(element_entity)

    def save_in_db(self, dto: ElementDTO) -> None:
        entity = self._element_mapper.map_from_dto_to_entity(dto)
        self._element_repository.save(entity)
        print("Element zapisany w BD")

    def update_by_id(self, dto: ElementDTO, entity_id: int) -> None:
        entity = self._element_mapper.map_from_dto_to_entity(dto)
        self._element_repository.update_by_id(entity, entity_id)
        print(f"Element o {entity_id} został zaktualizowany")

    def delete_by_id(self, entity_id: int) -> None:
        self._element_repository.delete_by_id(entity_id)
        print(f"Element o {entity_id} został usunięty")


