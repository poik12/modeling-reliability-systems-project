from typing import Tuple, List
from sqlalchemy import update, delete
from domain.models import System, Subsystem
from repository.abstract_repository import AbstractRepository


class SystemRepository(AbstractRepository):

    def __init__(self):
        super(SystemRepository, self).__init__()

    def find_all(self) -> List[Tuple[System]]:
        session = self._database_connector.create_session()
        return session.query(System).all()

    def find_by_id(self, entity_id: int) -> Tuple[System]:
        session = self._database_connector.create_session()
        return session.query(System).get(entity_id)

    def save(self, entity: System) -> None:
        session = self._database_connector.create_session()
        session.add(entity)
        for subsystem in entity.subsystem_list:
            subsystem_from_db = session.query(Subsystem).get(subsystem.id)
            entity.subsystems.append(subsystem_from_db)
        session.commit()

    def update_by_id(self, entity: System, entity_id: int) -> None:
        session = self._database_connector.create_session()
        data = {
            System.name: entity.name,
            System.reliability_structure: entity.reliability_structure,
            System.number_of_subsystems: entity.number_of_subsystems,
            System.updated_on: entity.updated_on,
            System.system_graph: entity.system_graph
        }
        statement = update(System).where(System.id == entity_id).values(data)
        session.execute(statement)

        system = session.query(System).get(entity_id)
        system.subsystems.clear()
        for subsystem in entity.subsystem_list:
            subsystem_from_db = session.query(Subsystem).get(subsystem.id)
            system.subsystems.append(subsystem_from_db)

        session.commit()

    def delete_by_id(self, entity_id: int) -> None:
        session = self._database_connector.create_session()
        system = session.query(System).get(entity_id)
        system.subsystems.clear()
        session.execute(delete(System).where(System.id == entity_id))
        session.commit()

