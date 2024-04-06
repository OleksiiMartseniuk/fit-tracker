from typing import Generic, TypeVar

from apps.utils.exception import BaseRepositoryException

ModelDTOType = TypeVar("ModelDTOType")


class DjangoCRUDMixin(Generic[ModelDTOType]):
    def get(self, **kwargs) -> ModelDTOType:
        return self.dto.from_model(self.model.objects.get(**kwargs))

    def get_all(self, **kwargs) -> list[ModelDTOType]:
        return [
            self.dto.from_model(item) for item in self.model.objects.filter(**kwargs)
        ]

    def create(self, **kwargs) -> ModelDTOType:
        return self.dto.from_model(self.model.objects.create(**kwargs))

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
        return self.dto.from_model(item)

    def delete(self, item_id: int) -> None:
        try:
            item = self.get(id=item_id)
        except self.model.DoesNotExist:
            raise BaseRepositoryException(
                f"Item with id {item_id} not found for model {self.model.__name__}"
            )
        item.delete()
