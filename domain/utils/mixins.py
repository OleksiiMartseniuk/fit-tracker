from typing import Generic, TypeVar

from domain.base.exception import BaseRepositoryException
from domain.utils.convertors import ConvertorModelToDTO

ModelDTOType = TypeVar("ModelDTOType")


class DjangoCRUDMixin(Generic[ModelDTOType]):
    def get(self, **kwargs) -> ModelDTOType:
        try:
            item = self.model.objects.get(**kwargs)
        except self.model.DoesNotExist:
            raise BaseRepositoryException(
                f"Item with id {kwargs} not found for model {self.model.__name__}"
            )
        return ConvertorModelToDTO.convert(item, self.dto)

    def get_or_none(self, **kwargs) -> ModelDTOType | None:
        item = self.model.objects.filter(**kwargs).first()
        return ConvertorModelToDTO.convert(item, self.dto) if item else None

    def get_all(self, **kwargs) -> list[ModelDTOType]:
        return [
            ConvertorModelToDTO.convert(item, self.dto)
            for item in self.model.objects.filter(**kwargs)
        ]

    def create(self, **kwargs) -> ModelDTOType:
        return ConvertorModelToDTO.convert(
            self.model.objects.create(**kwargs),
            self.dto,
        )

    def update(
        self,
        item_id: int,
        update_fields: bool = False,
        **kwargs,
    ) -> ModelDTOType:
        try:
            item = self.get(id=item_id)
        except self.model.DoesNotExist:
            raise BaseRepositoryException(
                f"Item with id {item_id} not found for model {self.model.__name__}"
            )

        for attr, value in kwargs.items():
            setattr(item, attr, value)

        item.save(update_fields=kwargs.keys()) if update_fields else item.save()
        return ConvertorModelToDTO.convert(item, self.dto)

    def delete(self, item_id: int) -> None:
        try:
            item = self.get(id=item_id)
        except self.model.DoesNotExist:
            raise BaseRepositoryException(
                f"Item with id {item_id} not found for model {self.model.__name__}"
            )
        item.delete()
