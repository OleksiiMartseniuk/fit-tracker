from typing import TypeVar

from django.db.models import Model
from django.forms.models import model_to_dict

ModelDTOType = TypeVar("ModelDTOType")


class ConvertorModelToDTO:
    @staticmethod
    def convert(model: Model, dto: ModelDTOType) -> ModelDTOType:
        return dto(**model_to_dict(model))
