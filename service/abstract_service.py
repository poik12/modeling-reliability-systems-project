from abc import ABC, abstractmethod
from typing import List


class AbstractService:

    @abstractmethod
    def get_all_from_db(self) -> List[object]:
        """Get all rows from entity."""

    @abstractmethod
    def get_by_id_from_db(self, entity_id: int) -> object:
        """Get entity from database by object id."""

    @abstractmethod
    def save_in_db(self, dto: object) -> None:
        """Save object in database."""

    @abstractmethod
    def update_by_id(self, dto: object, entity_id: int) -> None:
        """Update entity in database by object id."""

    @abstractmethod
    def delete_by_id(self, entity_id: int) -> None:
        """Delete entity from database by object id."""

