from typing import TypeVar, Type

from landscape_model_framework.abstract_entity import AbstractEntity, EntityMeta
from landscape_model_framework.exceptions import LoadingError

# annotation
mountain = TypeVar("mountain")


class Mountain(AbstractEntity, metaclass=EntityMeta):
    unicode_8_bit = "🗻"

    def __init__(self, idx=None):
        super().__init__(idx=idx, attributes=Mountain.default_attribute_map())

    @classmethod
    def load(cls: Type[mountain], dummy_mountain: dict) -> mountain:
        mountain = None
        if "id" in dummy_mountain:
            mountain = Mountain(dummy_mountain["id"])
        else:
            mountain = Mountain()
        if len(dummy_mountain["all_attrs"]) < 2:
            raise LoadingError(
                f"At least 2 of left, right, altitude need to be provided in {dummy_mountain} -> {mountain}."
            )
        missing_attr = None
        for attribute in mountain.custom_attributes:
            if attribute in dummy_mountain["all_attrs"]:
                value = dummy_mountain["all_attrs"][attribute]
                mountain.set_attribute(attribute, value)
            else:
                missing_attr = attribute
        if missing_attr == "left":
            mountain.left = int(mountain.right - 2 * mountain.altitude)
        elif missing_attr == "right":
            mountain.right = int(mountain.left + 2 * mountain.altitude)
        elif missing_attr == "altitude":
            mountain.altitude = int(0.5 * (mountain.right - mountain.left))
        return mountain

    @classmethod
    def default_attribute_map(cls):
        return {"left": 0, "right": 0, "altitude": 0}
