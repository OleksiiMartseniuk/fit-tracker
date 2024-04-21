from typing import Iterable, TypeVar

from django.db.models import Model
from django.forms.models import model_to_dict

ModelDTOType = TypeVar("ModelDTOType")


class ConvertorModelToDTO:
    @staticmethod
    def convert(
        model: Model,
        dto: ModelDTOType,
    ) -> "ModelDTOType":
        model_dict = model_to_dict(model)

        allow_fields = dto.__init__.__annotations__
        allow_fields.pop("return", None)

        data_dto = {}
        for filed in allow_fields.keys():
            if value := model_dict.get(filed):
                data_dto[filed] = value

        return dto(**data_dto)
