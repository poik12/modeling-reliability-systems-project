from sqlalchemy.sql import text
from typing import Tuple, List

from domain.models import Element
from repository.abstract_repository import AbstractRepository


class ElementRepository(AbstractRepository):
    """This repository consists of raw queries."""

    def __init__(self):
        super(ElementRepository, self).__init__()

    def find_all(self) -> List[Tuple[Element]]:
        connection = self._database_connector.get_connection_to_database()
        cursor = self._database_connector.get_cursor()
        statement = "SELECT * FROM elements"
        with connection:
            cursor.execute(statement)
        return cursor.fetchall()

    def find_by_id(self, entity_id: int) -> Tuple[Element]:
        connection = self._database_connector.get_connection_to_database()
        cursor = self._database_connector.get_cursor()
        statement = """SELECT * FROM elements WHERE id=%s"""
        with connection:
            cursor.execute(statement, (entity_id,))
        return cursor.fetchone()

    def save(self, entity: Element) -> None:
        connection = self._database_connector.get_connection_to_database()
        statement = text("""INSERT INTO elements(name, damage_intensity, 
                            repair_intensity, created_on, updated_on) 
                            VALUES(:name, :damage_intensity, :repair_intensity, 
                            :created_on, :updated_on)""")
        data = {
            'name': entity.name,
            'damage_intensity': entity.damage_intensity,
            'repair_intensity': entity.repair_intensity,
            'created_on': entity.created_on,
            'updated_on': entity.updated_on
        }
        with connection:
            connection.execute(statement, data)

    def update_by_id(self, entity: Element, entity_id: int) -> None:
        connection = self._database_connector.get_connection_to_database()
        statement = text("""UPDATE elements SET name = :name, damage_intensity = :damage_intensity,
                            repair_intensity = :repair_intensity, updated_on = :updated_on 
                            WHERE id = :id""")
        data = {
            'name': entity.name,
            'damage_intensity': entity.damage_intensity,
            'repair_intensity': entity.repair_intensity,
            'updated_on': entity.updated_on,
            'id': entity_id
        }
        with connection:
            connection.execute(statement, data)

    def delete_by_id(self, entity_id: int) -> None:
        connection = self._database_connector.get_connection_to_database()
        statement = text("""DELETE FROM elements WHERE id = :id""")
        data = {'id': entity_id}
        with connection:
            connection.execute(statement, data)

