from abc import ABC, abstractmethod
from typing import Generic, Iterable, TypeVar

TableDTOType = TypeVar("TableDTOType")


class Repository(Generic[TableDTOType], ABC):
    @abstractmethod
    def get(self, *args, **kwargs) -> TableDTOType:
        pass

    @abstractmethod
    def get_all(self, *args, **kwargs) -> Iterable[TableDTOType]:
        pass

    @abstractmethod
    def create(self, **kwargs) -> TableDTOType:
        pass

    @abstractmethod
    def update(self, id_item: int, **kwargs) -> TableDTOType:
        pass

    @abstractmethod
    def delete(self, id_item: int) -> None:
        pass
