from typing import TypeVar, Type
from python.landscape_model_framework.abstract_entity import AbstractEntity, EntityMeta

# annotation
tree = TypeVar('tree')


class Tree(AbstractEntity, metaclass=EntityMeta):
    unicode_8_bit = '🌳'

    def __init__(self, idx=None):
        super().__init__(
            idx=idx,
            attributes=Tree.default_attribute_map()
        )

    @classmethod
    def load(cls: Type[tree], str_repr: str) -> tree:
        print('loading Tree')

    @classmethod
    def default_attribute_map(cls):
        return {
            "center": 0,
            "height": 0
        }
