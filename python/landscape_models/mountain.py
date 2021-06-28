from typing import TypeVar, Type

from python.landscape_model_framework.abstract_entity import AbstractEntity, EntityMeta

# annotation
mountain = TypeVar('mountain')


class Mountain(AbstractEntity, metaclass=EntityMeta):
    unicode_8_bit = '🗻'

    def __init__(self, idx=None):
        super(Mountain, self).__init__(
            idx=idx,
            attributes=Mountain.default_attribute_map()

        )

    @classmethod
    def load(cls: Type[mountain], str_repr: str) -> mountain:
        print('loading Mountain')

    @classmethod
    def default_attribute_map(cls):
        return {
            "left": 0,
            "right": 0,
            "height": 0
        }
