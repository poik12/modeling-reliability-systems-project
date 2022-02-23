from abc import ABC, abstractmethod
from typing import Tuple, List
from domain.database_connection import DatabaseConnection


class AbstractRepository(ABC):

    @abstractmethod
    def __init__(self):
        self._database_connector = DatabaseConnection()

    @abstractmethod
    def find_all(self) -> List[Tuple[object]]:
        """Find all rows in entity."""

    @abstractmethod
    def find_by_id(self, entity_id: int) -> Tuple[object]:
        """Find row in entity by id."""

    @abstractmethod
    def save(self, entity: object) -> None:
        """Save new row in entity."""

    @abstractmethod
    def update_by_id(self, entity: object, entity_id: int) -> None:
        """Update row in entity by id."""

    @abstractmethod
    def delete_by_id(self, entity_id: int) -> None:
        """Delete row in entity by id."""

