from typing import TypeVar, Type

from python.models.abstract_entity import AbstractEntity, EntityMeta

# annotation
mountain = TypeVar('mountain')


class Mountain(AbstractEntity, metaclass=EntityMeta):
    ascii_key = "keymouontain"

    def __init__(self, idx=None):
        super(Mountain, self).__init__(
            idx=idx,
            attributes=
            {
                "left": 0,
                "right": 0,
                "height": 0
            }
        )

    @classmethod
    def load(cls: Type[mountain], str_repr: str) -> mountain:
        print('loading Mountain')
