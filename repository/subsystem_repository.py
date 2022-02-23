from sqlalchemy import update, delete
from typing import Tuple, List
from domain.models import Subsystem, Element
from repository.abstract_repository import AbstractRepository


class SubsystemRepository(AbstractRepository):

    def __init__(self):
        super(SubsystemRepository, self).__init__()

    def find_all(self) -> List[Tuple[Subsystem]]:
        session = self._database_connector.create_session()
        return session.query(Subsystem).all()

    def find_by_id(self, entity_id: int) -> Tuple[Subsystem]:
        session = self._database_connector.create_session()
        return session.query(Subsystem).get(entity_id)

    def save(self, entity: Subsystem) -> None:
        session = self._database_connector.create_session()
        session.add(entity)
        for element in entity.element_list:
            element_from_db = session.query(Element).get(element.id)
            entity.elements.append(element_from_db)
        session.commit()

    def update_by_id(self, entity: Subsystem, entity_id: int) -> None:
        session = self._database_connector.create_session()
        data = {
            Subsystem.name: entity.name,
            Subsystem.reliability_structure: entity.reliability_structure,
            Subsystem.number_of_elements: entity.number_of_elements,
            Subsystem.updated_on: entity.updated_on
        }
        statement = update(Subsystem).where(Subsystem.id == entity_id).values(data)
        session.execute(statement)

        subsystem = session.query(Subsystem).get(entity_id)
        subsystem.elements.clear()
        for element in entity.element_list:
            element_from_db = session.query(Element).get(element.id)
            subsystem.elements.append(element_from_db)

        session.commit()

    def delete_by_id(self, entity_id: int) -> None:
        session = self._database_connector.create_session()
        subsystem = session.query(Subsystem).get(entity_id)
        subsystem.elements.clear()
        session.execute(delete(Subsystem).where(Subsystem.id == entity_id))
        session.commit()



