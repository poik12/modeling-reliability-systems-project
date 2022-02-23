from typing import Tuple, List

from sqlalchemy import update, delete

from domain.models import Simulation
from repository.abstract_repository import AbstractRepository


class SimulationRepository(AbstractRepository):

    def __init__(self):
        super(SimulationRepository, self).__init__()

    def find_all(self) -> List[Tuple[Simulation]]:
        session = self._database_connector.create_session()
        return session.query(Simulation).all()

    def find_by_id(self, entity_id: int) -> Tuple[Simulation]:
        session = self._database_connector.create_session()
        return session.query(Simulation).get(entity_id)

    def save(self, entity: Simulation) -> None:
        session = self._database_connector.create_session()
        session.add(entity)
        session.commit()

    def update_by_id(self, entity: Simulation, entity_id: int) -> None:
        session = self._database_connector.create_session()
        data = {
            Simulation.name: entity.name,
            Simulation.system_id: entity.system_id,
            Simulation.time_horizon: entity.time_horizon,
            Simulation.time_change: entity.time_change,
            Simulation.time_repair: entity.time_repair,
            Simulation.number_of_iterations: entity.number_of_iterations,
            Simulation.updated_on: entity.updated_on
        }
        statement = update(Simulation).where(Simulation.id == entity_id).values(data)
        session.execute(statement)
        session.commit()

    def delete_by_id(self, entity_id: int) -> None:
        session = self._database_connector.create_session()
        session.execute(delete(Simulation).where(Simulation.id == entity_id))
        session.commit()

