from typing import TypeVar, Type
from python.models.abstract_entity import AbstractEntity, EntityMeta

# annotation
tree = TypeVar('tree')


class Tree(AbstractEntity, metaclass=EntityMeta):
    ascii_key = "dfskl"

    def __init__(self, idx=None):
        super().__init__(
            idx=idx,
            attributes=
            {
                "center": 0,
                "height": 0
            }
        )

    @classmethod
    def load(cls: Type[tree], str_repr: str) -> tree:
        print('loading Tree')
